filename_map = {
    'TX/agencies.csv': {
        'key': 'agencies',
        'uniq': 'AGENCY_ID',
        'cols': ['AGENCY_ID', 'ORI', 'NCIC_AGENCY_NAME', 'PUB_AGENCY_UNIT', 'STATE_ID', 'STATE_NAME', 'STATE_ABBR', 'DIVISION_CODE', 'DIVISION_NAME', 'REGION_CODE', 'REGION_NAME', 'AGENCY_TYPE_NAME', 'POPULATION', 'POPULATION_GROUP_ID', 'POPULATION_GROUP_CODE', 'POPULATION_GROUP_DESC', 'NIBRS_START_DATE', 'COUNTY_NAME', 'MSA_NAME'],
    },
    'TX/NIBRS_AGE.csv': {
        'key': 'NIBRS_AGE',
        'uniq': 'AGE_ID',
        'cols':	['AGE_ID', 'AGE_NAME'],
    },
    'TX/NIBRS_ARREST_TYPE.csv': {
        'key': 'NIBRS_ARREST_TYPE',
        'uniq': 'ARREST_TYPE_ID',
        'cols':	['ARREST_TYPE_ID', 'ARREST_TYPE_NAME'],
    },
    'TX/NIBRS_ARRESTEE_WEAPON.csv': {
        'key': 'NIBRS_ARRESTEE_WEAPON',
        'uniq': 'ARRESTEE_ID',
        'cols':	['ARRESTEE_ID', 'WEAPON_ID'],
    },
    'TX/NIBRS_ARRESTEE.csv': {
        'key': 'NIBRS_ARRESTEE',
        'uniq': 'INCIDENT_ID',
        'cols':	['AGE_ID', 'ARRESTEE_ID', 'INCIDENT_ID', 'ARRESTEE_SEQ_NUM', 'ARREST_DATE', 'MULTIPLE_INDICATOR', 'OFFENSE_TYPE_ID', 'AGE_NUM', 'SEX_CODE', 'RACE_ID', 'ETHNICITY_ID'],
    },
    'TX/NIBRS_CLEARED_EXCEPT.csv': {
        'key': 'NIBRS_CLEARED_EXCEPT',
        'uniq': 'CLEARED_EXCEPT_ID',
        'cols':	['CLEARED_EXCEPT_ID', 'CLEARED_EXCEPT_DESC'],
    },
    'TX/NIBRS_ETHNICITY.csv': {
        'key': 'NIBRS_ETHNICITY',
        'uniq': 'ETHNICITY_ID',
        'cols':	['ETHNICITY_ID', 'ETHNICITY_NAME'],
    },
    'TX/NIBRS_INJURY.csv': {
        'key': 'NIBRS_INJURY',
        'uniq': 'INJURY_ID',
        'cols':	['INJURY_ID', 'INJURY_NAME'],
    },
    'TX/NIBRS_LOCATION_TYPE.csv': {
        'key': 'NIBRS_LOCATION_TYPE',
        'uniq': 'LOCATION_ID',
        'cols':	['LOCATION_ID', 'LOCATION_NAME'],
    },
    'TX/NIBRS_OFFENDER.csv': {
        'key': 'NIBRS_OFFENDER',
        'uniq': 'INCIDENT_ID',
        'cols':	['AGE_ID', 'INCIDENT_ID', 'AGE_NUM', 'SEX_CODE', 'RACE_ID', 'ETHNICITY_ID', 'OFFENDER_ID', 'OFFENDER_SEQ_NUM'],
    },
    'TX/NIBRS_OFFENSE_TYPE.csv': {
        'key': 'NIBRS_OFFENSE_TYPE',
        'uniq': 'OFFENSE_TYPE_ID',
        'cols':	['OFFENSE_TYPE_ID', 'OFFENSE_NAME'],
    },
    'TX/NIBRS_OFFENSE.csv': {
        'key': 'NIBRS_OFFENSE',
        'uniq': 'INCIDENT_ID',
        'cols':	['INCIDENT_ID', 'OFFENSE_TYPE_ID', 'LOCATION_ID', 'OFFENSE_ID'],
    },
    'TX/NIBRS_RELATIONSHIP.csv': {
        'key': 'NIBRS_RELATIONSHIP',
        'uniq': 'RELATIONSHIP_ID',
        'cols':	['RELATIONSHIP_ID', 'RELATIONSHIP_NAME'],
    },
    'TX/NIBRS_SUSPECT_USING.csv': {
        'key': 'NIBRS_SUSPECT_USING',
        'uniq': 'OFFENSE_ID',
        'cols':	['OFFENSE_ID', 'SUSPECT_USING_ID'],
    },
    'TX/NIBRS_SUSPECTED_DRUG_TYPE.csv': {
        'key': 'NIBRS_SUSPECTED_DRUG_TYPE',
        'uniq': 'SUSPECTED_DRUG_TYPE_ID',
        'cols':	['SUSPECTED_DRUG_TYPE_ID', 'SUSPECTED_DRUG_NAME'],
    },
    'TX/NIBRS_SUSPECTED_DRUG.csv': {
        'key': 'NIBRS_SUSPECTED_DRUG',
        'uniq': 'SUSPECTED_DRUG_TYPE_ID',
        'cols':	['SUSPECTED_DRUG_TYPE_ID', 'EST_DRUG_QTY', 'DRUG_MEASURE_TYPE_ID'],
    },
    'TX/NIBRS_USING_LIST.csv': {
        'key': 'NIBRS_USING_LIST',
        'uniq': 'SUSPECT_USING_ID',
        'cols':	['SUSPECT_USING_ID', 'SUSPECT_USING_NAME'],
    },
    'TX/NIBRS_VICTIM_CIRCUMSTANCES.csv': {
        'key': 'NIBRS_VICTIM_CIRCUMSTANCES',
        'uniq': 'VICTIM_ID',
        'cols':	['CIRCUMSTANCES_ID', 'VICTIM_ID'],
    },
    'TX/NIBRS_VICTIM_INJURY.csv': {
        'key': 'NIBRS_VICTIM_INJURY',
        'uniq': 'VICTIM_ID',
        'cols':	['INJURY_ID', 'VICTIM_ID'],
    },
    'TX/NIBRS_VICTIM_OFFENDER_REL.csv': {
        'key': 'NIBRS_VICTIM_OFFENDER_REL',
        'uniq': 'VICTIM_ID',
        'cols':	['OFFENDER_ID', 'RELATIONSHIP_ID', 'VICTIM_ID'],
    },
    'TX/NIBRS_VICTIM_OFFENSE.csv': {
        'key': 'NIBRS_VICTIM_OFFENSE',
        'uniq': 'VICTIM_ID',
        'cols':	['OFFENSE_ID', 'VICTIM_ID'],
    },
    'TX/NIBRS_VICTIM_TYPE.csv': {
        'key': 'NIBRS_VICTIM_TYPE',
        'uniq': 'VICTIM_TYPE_ID',
        'cols':	['VICTIM_TYPE_ID', 'VICTIM_TYPE_NAME'],
    },
    'TX/NIBRS_VICTIM.csv': {
        'key': 'NIBRS_VICTIM',
        'uniq': 'INCIDENT_ID',
        'cols':	['AGE_ID', 'INCIDENT_ID', 'AGE_NUM', 'SEX_CODE', 'RACE_ID', 'ETHNICITY_ID', 'VICTIM_ID', 'VICTIM_TYPE_ID', 'VICTIM_SEQ_NUM'],
    },
    'TX/NIBRS_WEAPON_TYPE.csv': {
        'key': 'NIBRS_WEAPON_TYPE',
        'uniq': 'WEAPON_ID',
        'cols':	['WEAPON_ID', 'WEAPON_NAME'],
    },
    'TX/NIBRS_WEAPON.csv': {
        'key': 'NIBRS_WEAPON',
        'uniq': 'OFFENSE_ID',
        'cols':	['WEAPON_ID', 'OFFENSE_ID'],
    },
    'TX/REF_RACE.csv': {
        'key': 'REF_RACE',
        'uniq': 'RACE_ID',
        'cols':	['RACE_ID', 'RACE_DESC'],
    },
}

def key_exists(key):
    return key in filename_map

def get_data(key):
    return filename_map[key]