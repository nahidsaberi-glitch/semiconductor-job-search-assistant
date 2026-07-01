TARGET_COMPANIES = [
    "Intel", "AMD", "NVIDIA", "Apple", "Qualcomm", "Broadcom", "Marvell", "Cisco",
    "Micron", "Western Digital", "Seagate",
    "Texas Instruments", "Analog Devices", "Skyworks Solutions", "Qorvo",
    "NXP Semiconductors", "onsemi", "Infineon",
    "GlobalFoundries", "Tower Semiconductor", "TSMC",
    "Applied Materials", "Lam Research", "KLA", "ASML",
    "Advantest", "Teradyne", "Keysight",
    "Cadence", "Synopsys",
    "SiTime", "Bosch",
    "Astera Labs", "Ayar Labs", "Rambus"
]

CAREER_PATHS = {
    "DFT / Test Engineering": [
        "DFT", "scan", "scan logic", "scan compression", "ATPG", "TATPG",
        "MBIST", "LBIST", "JTAG", "IJTAG", "boundary scan", "BIST",
        "test compression", "stuck-at fault", "transition fault",
        "cell-aware test", "fault coverage", "pattern generation",
        "pattern reduction", "wafer sort", "ATE", "Advantest", "Teradyne",
        "test program", "test development", "production test"
    ],
    "Product Engineering": [
        "product engineer", "product development engineer", "yield analysis",
        "yield improvement", "wafer sort", "ATE", "high volume manufacturing",
        "production", "NPI", "test cost reduction", "DPPM", "PRQ",
        "product qualification", "data analysis", "manufacturing support"
    ],
    "Validation Engineering": [
        "validation engineer", "silicon validation", "post-silicon validation",
        "system validation", "bring-up", "characterization", "debug",
        "Python", "automation", "lab validation", "SoC", "CPU", "GPU",
        "PCIe", "DDR", "HBM", "high speed", "board bring-up"
    ],
    "Reliability Engineering": [
        "reliability engineer", "HTOL", "HAST", "uHAST", "THB", "TC",
        "HTSL", "burn-in", "JEDEC", "qualification", "failure analysis",
        "root cause analysis", "infant mortality", "wear-out", "FIT",
        "MTTF", "DPPM", "ESD", "latch-up", "corrosion",
        "moisture sensitivity", "MSL", "package reliability", "reliability testing"
    ],
    "Manufacturing / NPI": [
        "manufacturing engineer", "NPI", "process engineer", "OSAT",
        "assembly", "packaging", "high volume manufacturing",
        "process control", "SPC", "yield ramp", "production ramp",
        "factory", "operations", "supply chain"
    ],
    "Packaging Engineering": [
        "packaging engineer", "package reliability", "assembly",
        "substrate", "wire bond", "flip chip", "BGA", "thermal",
        "moisture", "MSL", "reflow", "package qualification",
        "advanced packaging", "2.5D", "3D packaging"
    ],
    "Applications Engineering": [
        "applications engineer", "field applications engineer", "FAE",
        "customer support", "technical support", "pre-sales",
        "post-sales", "debug", "customer issue", "silicon debug",
        "customer engineering"
    ],
    "Process Engineering": [
        "process engineer", "process integration", "process development",
        "lithography", "etch", "deposition", "CMP", "thin films",
        "metrology", "fab", "semiconductor process"
    ],
    "Failure Analysis": [
        "failure analysis", "FA", "root cause", "debug", "RMA",
        "SEM", "TEM", "FIB", "curve trace", "electrical failure analysis",
        "physical failure analysis", "8D", "corrective action"
    ],
    "Yield Engineering": [
        "yield engineer", "yield analysis", "yield improvement",
        "wafer sort", "data analysis", "JMP", "SQL", "Python",
        "SPC", "Pareto", "defect density", "binning", "sort data"
    ],
}

CAREER_PATH_ROLE_QUERIES = {
    "DFT / Test Engineering": ["DFT engineer", "test engineer", "ATPG engineer", "scan engineer", "wafer sort engineer", "ATE engineer", "test development engineer"],
    "Product Engineering": ["product engineer", "product development engineer", "yield engineer"],
    "Validation Engineering": ["validation engineer", "post silicon validation engineer", "silicon validation engineer", "system validation engineer"],
    "Reliability Engineering": ["reliability engineer", "qualification engineer", "failure analysis engineer"],
    "Manufacturing / NPI": ["manufacturing engineer", "NPI engineer", "process engineer"],
    "Packaging Engineering": ["packaging engineer", "package reliability engineer"],
    "Applications Engineering": ["applications engineer", "field applications engineer", "FAE"],
    "Process Engineering": ["process engineer", "process integration engineer", "process development engineer"],
    "Failure Analysis": ["failure analysis engineer", "product failure analysis engineer"],
    "Yield Engineering": ["yield engineer", "yield analysis engineer", "product yield engineer"],
}

COMPANY_BOOSTS = {
    "intel": 20, "sitime": 18, "kla": 18, "advantest": 18,
    "amd": 16, "samsung": 15, "applied materials": 15, "teradyne": 15,
    "cisco": 12, "marvell": 12, "broadcom": 12, "qualcomm": 12,
    "lam research": 12, "micron": 12, "texas instruments": 12,
    "analog devices": 12, "skyworks": 12, "qorvo": 12, "onsemi": 12,
    "nxp": 12, "infineon": 12, "globalfoundries": 12,
    "tower semiconductor": 12, "tsmc": 15, "western digital": 10,
    "seagate": 10, "astera labs": 10, "ayar labs": 10, "rambus": 10,
    "bosch": 10, "keysight": 10, "nvidia": 10, "apple": 10,
    "cadence": 10, "synopsys": 10, "asml": 12,
}

CAREER_SITE_URLS = {
    "Intel": "https://jobs.intel.com/",
    "AMD": "https://careers.amd.com/",
    "NVIDIA": "https://www.nvidia.com/en-us/about-nvidia/careers/",
    "Apple": "https://jobs.apple.com/",
    "Qualcomm": "https://careers.qualcomm.com/",
    "Broadcom": "https://careers.broadcom.com/",
    "Marvell": "https://www.marvell.com/company/careers.html",
    "Cisco": "https://jobs.cisco.com/",
    "Micron": "https://www.micron.com/about/careers",
    "Western Digital": "https://jobs.westerndigital.com/",
    "Seagate": "https://careers.seagate.com/",
    "Texas Instruments": "https://careers.ti.com/",
    "Analog Devices": "https://careers.analog.com/",
    "Skyworks Solutions": "https://careers.skyworksinc.com/",
    "Qorvo": "https://careers.qorvo.com/",
    "NXP Semiconductors": "https://www.nxp.com/company/about-nxp/careers",
    "onsemi": "https://www.onsemi.com/company/careers",
    "Infineon": "https://www.infineon.com/careers",
    "GlobalFoundries": "https://gf.com/careers/",
    "Tower Semiconductor": "https://towersemi.com/careers/",
    "TSMC": "https://careers.tsmc.com/",
    "Applied Materials": "https://careers.appliedmaterials.com/",
    "Lam Research": "https://careers.lamresearch.com/",
    "KLA": "https://careers.kla.com/",
    "ASML": "https://www.asml.com/en/careers",
    "Advantest": "https://www.advantest.com/careers/",
    "Teradyne": "https://www.teradyne.com/careers/",
    "Keysight": "https://jobs.keysight.com/",
    "Cadence": "https://www.cadence.com/en_US/home/company/careers.html",
    "Synopsys": "https://careers.synopsys.com/",
    "SiTime": "https://www.sitime.com/company/careers",
    "Bosch": "https://www.bosch.com/careers/",
    "Astera Labs": "https://www.asteralabs.com/careers/",
    "Ayar Labs": "https://www.ayar.com/careers/",
    "Rambus": "https://www.rambus.com/careers/",
}

BAY_AREA_TERMS = [
    "san jose", "santa clara", "sunnyvale", "mountain view", "cupertino",
    "palo alto", "milpitas", "fremont", "san francisco", "san mateo",
    "redwood city", "menlo park", "newark", "hayward", "pleasanton",
    "bay area", "silicon valley", "san bruno", "south san francisco"
]

# Version 3.0 native career connector configuration.
# These connectors call public company/ATS job feeds directly instead of using Google or SerpAPI.
NATIVE_CAREER_CONNECTORS = {
    "Intel": {
        "type": "workday",
        "base_url": "https://intel.wd1.myworkdayjobs.com",
        "tenant": "intel",
        "site": "External",
        "site_url": "https://intel.wd1.myworkdayjobs.com/External",
    },
    "KLA": {
        "type": "workday",
        "base_url": "https://kla.wd1.myworkdayjobs.com",
        "tenant": "kla",
        "site": "UR",
        "site_url": "https://kla.wd1.myworkdayjobs.com/UR",
    },
    "NVIDIA": {
        "type": "workday",
        "base_url": "https://nvidia.wd5.myworkdayjobs.com",
        "tenant": "nvidia",
        "site": "NVIDIAExternalCareerSite",
        "site_url": "https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite",
    },
    "SiTime": {
        "type": "sitime_site",
        "url": "https://www.sitime.com/job-listings",
    },
    # Ready to enable after endpoint verification:
    # "AMD": {
    #     "type": "workday",
    #     "base_url": "https://amd.wd5.myworkdayjobs.com",
    #     "tenant": "amd",
    #     "site": "Careers",
    #     "site_url": "https://amd.wd5.myworkdayjobs.com/Careers",
    # },
}
