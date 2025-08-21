# version names etc
BW_PROJECTNAME = "costs_paper_2.1.0.dev5"
EI_VERSION = "3.9.1"
premise_version = "2.3.0.dev1"
BW_PROJECTNAME_BATTERIES = "premise_runs_{}_{}".format(EI_VERSION, premise_version)

# scenarios to be run
SCENARIOS = ["SSP2-NPi", "SSP2-PkBudg500"]
SCENARIOS_BATTERIES = ["SSP2-NPi", "SSP2-PkBudg650"]
SCEN2BATSCEN = {
    "SSP2-NPi": "SSP2-NPi",
    "SSP2-PkBudg500": "SSP2-PkBudg650"
}
YEARS = [2020, 2030, 2040, 2050]

# unit choices
EURO_REF_YEAR = 2022

REMIND_REGIONS = [
    "CAZ",
    "CHA",
    "EUR",
    "IND",
    "JPN",
    "LAM",
    "MEA",
    "NEU",
    "OAS",
    "REF",
    "SSA",
    "USA"
]

MC_SAMPLE_SIZE = 2000
MC_SAMPLE_SIZE_LARGER = 20000

TAKE_OUT_FOSSIL_RESOURCES_MIDPOINT = True