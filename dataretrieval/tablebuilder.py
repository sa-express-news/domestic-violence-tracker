from functools import reduce

from datagenerator import DataGenerator


def merge_hashes(*argv):
    return reduce(lambda x, y: {**x, **y}, argv, {})


def make_int(prop):
    try:
        prop = int(prop)
    except:
        if prop is not None and prop is not '':
            print(f'Prop: {prop} is not an interger!')
    finally:
        return prop


class TableBuilder():
    """All funtionality in this class is expected to be utilized inside a loop
        created through the DataGenerator, which iterates over incidents for a
        year/state. The exception is run_data_generator, which is syntactical
        sugar for the DataGenerator method.
    """
    def __init__(self, state, year):
        self.state = state
        self.year = year
        self._data_generator = DataGenerator(state, year)
        self.dv_like_relationships = set([27, 3, 4, 6, 12, 21, 26])
        self.violent_offenses = set([1, 3, 4, 27, 32, 36, 38, 43, 51])
        self._tables = {}

    def __getattr__(self, attr):
        return getattr(self._data_generator, attr)

    def run_data_generator(self):
        """Just syntactical sugar"""
        return self.run_generator()

    """The next five methods help us filter down to just DV incidents"""
    def is_classified_as_dv(self, victim):
        circumstances = self._get_hash_list('nibrs_victim_circumstances', victim['victim_id'])
        if circumstances is not None:
            return (any(circumstance['circumstances_id'] == '6' for circumstance in circumstances))
        else:
            return False

    def is_related_to_offender(self, victim):
        relationships = self._get_hash_list('nibrs_victim_offender_rel', victim['victim_id'])
        if relationships is not None:
            return any(int(relationship['relationship_id']) in self.dv_like_relationships for relationship in relationships)
        else:
            return False

    def is_violent_offense(self, incident):
        offenses = self._get_hash_list('nibrs_offense', incident['incident_id'])
        if offenses is not None:
            return any(int(offense['offense_type_id']) in self.violent_offenses for offense in offenses)
        else:
            return False

    def victim_is_person(self, victim):
        return victim['victim_type_id'] == '4' or victim['victim_type_id'] == '5'

    def is_domestic_violence(self, incident):
        victims = self._get_hash_list('nibrs_victim', incident['incident_id'])
        if victims is not None:
            for victim in victims:
                if (self.victim_is_person(victim) and
                   (self.is_classified_as_dv(victim) or (self.is_related_to_offender(victim) and self.is_violent_offense(incident)))):
                    return True
            return False
        else:
            return False

    """The next two methods are for aquiring hashes require additional complexities not
        provided in the generic getters from DataGenerator
    """
    def _get_agency_fields(self, id):
        agency = self._get_hash_list('agencies', id)[0]  # Sometimes there are multiple listings for agencies
        return {
            'agency_name': agency.get('ncic_agency_name'),
            'ori': agency.get('ori'),
            'county_name': agency.get('county_name'),
            'state_id': agency.get('state_id'),
            'state_abbr': agency.get('state_abbr'),
            'population': agency.get('population'),
            'population_group_code': agency.get('population_group_code'),
            'population_group_desc': agency.get('population_group_desc'),
            'nibrs_start_date': agency.get('nibrs_start_date'),
        }

    def _get_relationship_fields(self, victim_id):
        victim_offender_rel = self._get_hash_list('nibrs_victim_offender_rel', victim_id)
        if victim_offender_rel is not None:
            rel = next(
                (i for i in victim_offender_rel if i['relationship_id'] in self.dv_like_relationships),
                victim_offender_rel[0]
            )
            return self._get_hash('nibrs_relationship', rel['relationship_id'])
        else:
            return {}

    """These last five methods are used for actually building table rows.
        They should be called everytime the generator iterates to a new incident
        Allowing us to populate each table for each incident in generator
    """
    def add_incident_row(self, raw):
        if 'incidents' not in self._tables:
            self._tables['incidents'] = []

        try:
            incident = {
                'id': make_int(raw.get('incident_id')),
                'cleared_except_id': make_int(raw.get('cleared_except_id')),
                'cleared_except_desc': None,
                'agency_id': make_int(raw.get('agency_id')),
                'data_year': self.year,
                'submission_date': raw.get('submission_date'),
                'incident_date': raw.get('incident_date'),
            }

            """Grab other hashes via unique ID"""
            cleared_except = self._get_hash('nibrs_cleared_except', 'cleared_except_id')

            """Hash that requires custom functionality to obtain"""
            agency_fields = self._get_agency_fields(raw.get('agency_id'))

            self._tables['incidents'].append(
                merge_hashes(
                    incident,
                    cleared_except,
                    agency_fields
                )
            )
        except Exception as e:
            print(f'Failed to add row with id: {raw["incident_id"]} to incident table due to: {e}')

    def add_victim_rows(self, incident):
        if 'victims' not in self._tables:
            self._tables['victims'] = []

        try:
            victims = self._get_hash_list('nibrs_victim', incident['incident_id'])
            if victims is not None:
                for raw in victims:
                    victim = {
                        'id': make_int(raw.get('victim_id')),
                        'incident_id': make_int(raw.get('incident_id')),
                        'age_num': make_int(raw.get('age_num')),
                        'sex_code': raw.get('sex_code'),
                        'race_id': make_int(raw.get('race_id')),
                        'race_desc': None,
                        'ethnicity_id': make_int(raw.get('ethnicity_id')),
                        'ethnicity_name': None,
                        'victim_seq_num': make_int(raw.get('victim_seq_num')),
                        'injury_id': make_int(raw.get('injury_id')),
                        'injury_name': None,
                        'relationship_id': make_int(raw.get('relationship_id')),
                        'relationship_name': None,
                        'circumstances_id': make_int(raw.get('circumstance_id')),
                        'circumstances_name': None,
                    }

                    """Grab other hashes via unique ID"""
                    race = self._get_hash('ref_race', raw.get('race_id'))
                    ethnicity = self._get_hash('nibrs_ethnicity', raw.get('ethnicity_id'))

                    """Grab hashes that require stepping through a ref hash to find"""
                    injury = self._get_hash_through_reference(
                        'nibrs_victim_injury',
                        raw.get('victim_id'),
                        'nibrs_injury',
                        'injury_id'
                    )
                    circumstance = self._get_hash_through_reference(
                        'nibrs_victim_circumstances',
                        raw.get('victim_id'),
                        'nibrs_circumstances',
                        'circumstances_id'
                    )

                    """Hash that requires custom functionality to obtain"""
                    relationship = self._get_relationship_fields(raw.get('victim_id'))

                    self._tables['victims'].append(
                        merge_hashes(
                            victim,
                            race,
                            ethnicity,
                            injury,
                            relationship,
                            circumstance
                        )
                    )
        except Exception as e:
            print(f'Failed to add row with id: {incident["incident_id"]} to victims table due to: {e}')

    def add_offender_rows(self, incident):
        if 'offenders' not in self._tables:
            self._tables['offenders'] = []

        try:
            offenders = self._get_hash_list('nibrs_offender', incident['incident_id'])
            if offenders is not None:
                for raw in offenders:
                    offender = {
                        'id': make_int(raw.get('offender_id')),
                        'incident_id': make_int(raw.get('incident_id')),
                        'age_num': make_int(raw.get('age_num')),
                        'sex_code': raw.get('sex_code'),
                        'race_id': make_int(raw.get('race_id')),
                        'race_desc': None,
                        'ethnicity_id': make_int(raw.get('ethnicity_id')),
                        'ethnicity_name': None,
                        'offender_seq_num': make_int(raw.get('offender_seq_num')),
                    }

                    """Grab other hashes via unique ID"""
                    race = self._get_hash('ref_race', raw.get('race_id'))
                    ethnicity = self._get_hash('nibrs_ethnicity', raw.get('ethnicity_id'))

                    self._tables['offenders'].append(
                        merge_hashes(
                            offender,
                            race,
                            ethnicity
                        )
                    )
        except Exception as e:
            print(f'Failed to add row with id: {incident["incident_id"]} to offenders table due to: {e}')

    def add_offense_rows(self, incident):
        if 'offenses' not in self._tables:
            self._tables['offenses'] = []

        try:
            offenses = self._get_hash_list('nibrs_offense', incident['incident_id'])
            if offenses is not None:
                for raw in offenses:
                    offense = {
                        'id': make_int(raw.get('offense_id')),
                        'incident_id': make_int(raw.get('incident_id')),
                        'location_id': make_int(raw.get('location_id')),
                        'location_name': None,
                        'offense_type_id': make_int(raw.get('offense_type_id')),
                        'offense_name': None,
                        'weapon_id': None,
                        'weapon_name': None,
                        'suspect_using_id': None,
                        'suspect_using_name': None,
                    }

                    """Grab other hashes via unique ID"""
                    location = self._get_hash('nibrs_location_type', raw.get('location_id'))
                    offense_type = self._get_hash('nibrs_offense_type', raw.get('offense_type_id'))

                    """Grab hashes that require stepping through a ref hash to find"""
                    weapon = self._get_hash_through_reference(
                        'nibrs_weapon',
                        raw.get('offense_id'),
                        'nibrs_weapon_type',
                        'weapon_id'
                    )
                    suspect_using = self._get_hash_through_reference(
                        'nibrs_suspect_using',
                        raw.get('offense_id'),
                        'nibrs_using_list',
                        'suspect_using_id'
                    )

                    self._tables['offenses'].append(
                        merge_hashes(
                            offense,
                            location,
                            offense_type,
                            weapon,
                            suspect_using
                        )
                    )
        except Exception as e:
            print(f'Failed to add row with id: {incident["incident_id"]} to offenses table due to: {e}')

    def add_arrestee_rows(self, incident):
        if 'arrestees' not in self._tables:
            self._tables['arrestees'] = []

        try:
            arrestees = self._get_hash_list('nibrs_arrestee', incident['incident_id'])
            if arrestees is not None:
                for raw in arrestees:
                    arrestee = {
                        'id': make_int(raw.get('arrestee_id')),
                        'incident_id': make_int(raw.get('incident_id')),
                        'arrestee_seq_num': make_int(raw.get('arrestee_seq_num')),
                        'arrest_date': raw.get('arrest_date'),
                        'multiple_indicator': raw.get('multiple_indicator'),
                        'offense_type_id': make_int(raw.get('offense_type_id')),
                        'offense_name': None,
                        'age_num': make_int(raw.get('age_num')),
                        'sex_code': raw.get('sex_code'),
                        'race_id': make_int(raw.get('race_id')),
                        'race_desc': None,
                        'ethnicity_id': make_int(raw.get('ethnicity_id')),
                        'ethnicity_name': None,
                        'offender_seq_num': make_int(raw.get('offender_seq_num')),
                    }

                    """Grab other hashes via unique ID"""
                    offense_type = self._get_hash('nibrs_offense_type', raw.get('offense_type_id'))
                    race = self._get_hash('ref_race', raw.get('race_id'))
                    ethnicity = self._get_hash('nibrs_ethnicity', raw.get('ethnicity_id'))

                    self._tables['arrestees'].append(
                        merge_hashes(
                            arrestee,
                            offense_type,
                            race,
                            ethnicity
                        )
                    )
        except Exception as e:
            print(f'Failed to add row with id: {incident["incident_id"]} to arrestees table due to: {e}')

    def populate_tables(self, incident):
        self.add_incident_row(incident)
        self.add_victim_rows(incident)
        self.add_offender_rows(incident)
        self.add_offense_rows(incident)
        self.add_arrestee_rows(incident)

    def eject_table(self, table):
        return self._tables[table]

    def eject_all_tables(self):
        for name, table in self._tables.items():
            yield {
                'name': f'{name}',
                'filename': f'{name}-{self.state}-{self.year}',
                'table': table,
            }
