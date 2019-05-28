filename_map = {
    'agencies.csv': {
        'key': 'agencies',
        'uniq': 'agency_id',
        'cols': ['agency_id', 'ori', 'ncic_agency_name', 'state_id', 'state_abbr', 'population', 'population_group_code', 'population_group_desc', 'nibrs_start_date', 'county_name'],
    },
    'cde_agencies.csv': {
        'key': 'agencies',
        'uniq': 'agency_id',
        'cols': ['agency_id', 'ori', 'agency_name', 'state_id', 'state_abbr', 'population', 'population_group_code', 'population_group_desc', 'start_year', 'primary_county'],
        'map_cols_to': 'agencies.csv'
    },
    'nibrs_age.csv': {
        'key': 'nibrs_age',
        'uniq': 'age_id',
        'cols': ['age_id', 'age_name'],
    },
    'nibrs_arrest_type.csv': {
        'key': 'nibrs_arrest_type',
        'uniq': 'arrest_type_id',
        'cols': ['arrest_type_id', 'arrest_type_name'],
    },
    'nibrs_arrestee_weapon.csv': {
        'key': 'nibrs_arrestee_weapon',
        'uniq': 'arrestee_id',
        'cols': ['arrestee_id', 'weapon_id'],
    },
    'nibrs_arrestee.csv': {
        'key': 'nibrs_arrestee',
        'uniq': 'incident_id',
        'cols': ['age_id', 'arrestee_id', 'incident_id', 'arrestee_seq_num', 'arrest_date', 'multiple_indicator', 'offense_type_id', 'age_num', 'sex_code', 'race_id', 'ethnicity_id'],
    },
    'nibrs_cleared_except.csv': {
        'key': 'nibrs_cleared_except',
        'uniq': 'cleared_except_id',
        'cols': ['cleared_except_id', 'cleared_except_desc'],
    },
    'nibrs_ethnicity.csv': {
        'key': 'nibrs_ethnicity',
        'uniq': 'ethnicity_id',
        'cols': ['ethnicity_id', 'ethnicity_name'],
    },
    'nibrs_injury.csv': {
        'key': 'nibrs_injury',
        'uniq': 'injury_id',
        'cols': ['injury_id', 'injury_name'],
    },
    'nibrs_location_type.csv': {
        'key': 'nibrs_location_type',
        'uniq': 'location_id',
        'cols': ['location_id', 'location_name'],
    },
    'nibrs_offender.csv': {
        'key': 'nibrs_offender',
        'uniq': 'incident_id',
        'cols': ['age_id', 'incident_id', 'age_num', 'sex_code', 'race_id', 'ethnicity_id', 'offender_id', 'offender_seq_num'],
    },
    'nibrs_offense_type.csv': {
        'key': 'nibrs_offense_type',
        'uniq': 'offense_type_id',
        'cols': ['offense_type_id', 'offense_name'],
    },
    'nibrs_offense.csv': {
        'key': 'nibrs_offense',
        'uniq': 'incident_id',
        'cols': ['incident_id', 'offense_type_id', 'location_id', 'offense_id'],
    },
    'nibrs_relationship.csv': {
        'key': 'nibrs_relationship',
        'uniq': 'relationship_id',
        'cols': ['relationship_id', 'relationship_name'],
    },
    'nibrs_suspect_using.csv': {
        'key': 'nibrs_suspect_using',
        'uniq': 'offense_id',
        'cols': ['offense_id', 'suspect_using_id'],
    },
    'nibrs_suspected_drug_type.csv': {
        'key': 'nibrs_suspected_drug_type',
        'uniq': 'suspected_drug_type_id',
        'cols': ['suspected_drug_type_id', 'suspected_drug_name'],
    },
    'nibrs_suspected_drug.csv': {
        'key': 'nibrs_suspected_drug',
        'uniq': 'suspected_drug_type_id',
        'cols': ['suspected_drug_type_id', 'est_drug_qty', 'drug_measure_type_id'],
    },
    'nibrs_using_list.csv': {
        'key': 'nibrs_using_list',
        'uniq': 'suspect_using_id',
        'cols': ['suspect_using_id', 'suspect_using_name'],
    },
    'nibrs_victim_circumstances.csv': {
        'key': 'nibrs_victim_circumstances',
        'uniq': 'victim_id',
        'cols': ['circumstances_id', 'victim_id'],
    },
    'nibrs_victim_injury.csv': {
        'key': 'nibrs_victim_injury',
        'uniq': 'victim_id',
        'cols': ['injury_id', 'victim_id'],
    },
    'nibrs_victim_offender_rel.csv': {
        'key': 'nibrs_victim_offender_rel',
        'uniq': 'victim_id',
        'cols': ['offender_id', 'relationship_id', 'victim_id'],
    },
    'nibrs_victim_offense.csv': {
        'key': 'nibrs_victim_offense',
        'uniq': 'victim_id',
        'cols': ['offense_id', 'victim_id'],
    },
    'nibrs_victim_type.csv': {
        'key': 'nibrs_victim_type',
        'uniq': 'victim_type_id',
        'cols': ['victim_type_id', 'victim_type_name'],
    },
    'nibrs_victim.csv': {
        'key': 'nibrs_victim',
        'uniq': 'incident_id',
        'cols': ['age_id', 'incident_id', 'age_num', 'sex_code', 'race_id', 'ethnicity_id', 'victim_id', 'victim_type_id', 'victim_seq_num'],
    },
    'nibrs_weapon_type.csv': {
        'key': 'nibrs_weapon_type',
        'uniq': 'weapon_id',
        'cols': ['weapon_id', 'weapon_name'],
    },
    'nibrs_weapon.csv': {
        'key': 'nibrs_weapon',
        'uniq': 'offense_id',
        'cols': ['weapon_id', 'offense_id'],
    },
    'ref_race.csv': {
        'key': 'ref_race',
        'uniq': 'race_id',
        'cols': ['race_id', 'race_desc'],
    },
}


def key_exists(key):
    return key in filename_map


def map_col_name(lookup, idx):
    try:
        return filename_map[lookup['map_cols_to']]['cols'][idx]
    except:
        print(f'Problem mapping lookup: {lookup["key"]} with idx: {idx}')


def get_data(key):
    return filename_map[key]
