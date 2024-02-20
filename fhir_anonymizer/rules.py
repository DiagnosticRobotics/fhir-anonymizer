from fhir_anonymizer.anonymizers import *

patient = {
    '$.name[*].family': mask(),
    '$.name[*].given[*]': mask(),
    '$.address[*].line[*]':  mask(),
    '$.address[*].city':  mask(),
    '$.address[*].postalCode' : mask("9970000"),
    #'$.birthDate': shift_time() ,
    '$.identifier[*].value': hash_string()
}

coverage = {
    '$.subscriberId': hash_string(),
    '$.identifier[*].value': hash_string()
}

explanation_of_benefit = {
    '$.identifier[*].value': hash_string(),
    '$.provider.identifier.value': hash_string(),
    '$.organization.identifier.value': hash_string(),
    '$.facility.identifier.value': hash_string(),
    '$.careTeam[*].provider.identifier.value': hash_string(),
}

rules = {
    "Patient": patient,
    "Coverage": coverage,
    "ExplanationOfBenefit": explanation_of_benefit
}