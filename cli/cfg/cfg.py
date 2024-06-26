from pathlib import Path

root = Path(__file__).parent.parent.parent

definitions = {
    "Dasyprocta": "Agouti (rodent)",
    "Bos": "Cattle (including domesticated cows and wild bison)",
    "Pecari": "Peccary (pig-like mammal native to the Americas)",
    "Mazama": "Brocket (small deer)",
    "Cuniculus": "Rabbit or hare",
    "Leptotila": "Dove (often found in tropical and subtropical regions)",
    "Human": "Homo sapiens (us!)",
    "Aramides": "Wood rail or forest rail (bird species)",
    "Tinamus": "Ground-dwelling bird native to Central and South America",
    "Eira": "Tayra (weasel-like mammal)",
    "Crax": "Curassow (large bird found in forests)",
    "Procyon": "Raccoon",
    "Capra": "Goat (both domesticated and wild)",
    "Dasypus": "Armadillo",
    "Sciurus": "Squirrel",
    "Crypturellus": "Forest tinamou (bird)",
    "Tamandua": "Anteater found in South America",
    "Proechimys": "Spiny rat (native to the Neotropics)",
    "Leopardus": "Small wild cat (including ocelots and margays)",
    "Equus": "Horse, zebra, or donkey",
    "Columbina": "Dove or pigeon",
    "Nyctidromus": "Nightjar or goatsucker (bird)",
    "Ortalis": "Chachalaca or guan (bird)",
    "Emballonura": "Sheath-tailed bat",
    "Odontophorus": "Quail (bird found in the Americas)",
    "Geotrygon": "Quail dove (another pigeon genus)",
    "Metachirus": "Mouse opossum",
    "Catharus": "Thrush (such as the hermit thrush)",
    "Cerdocyon": "Crab-eating fox",
    "Momotus": "Motmot (colorful bird found in the tropics)",
    "Tapirus": "Tapir (large herbivorous mammal)",
    "Canis": "Wolf, domestic dog, or other canids",
    "Furnarius": "Ovenbird (known for nest-building skills)",
    "Didelphis": "Opossum",
    "Sylvilagus": "Cottontail rabbit",
    "Unknown": "Unidentified species (mysterious!)",
}

short_names = {
    "Dasyprocta": "Rodent",
    "Bos": "Cattle",
    "Pecari": "Boar",
    "Mazama": "Deer",
    "Cuniculus": "Rabbit",
    "Leptotila": "Dove",
    "Human": "Human",
    "Aramides": "Bird",
    "Tinamus": "Ground bird",
    "Eira": "Weasel",
    "Crax": "Large bird",
    "Procyon": "Raccoon",
    "Capra": "Goat",
    "Dasypus": "Armadillo",
    "Sciurus": "Squirrel",
    "Crypturellus": "Forest bird",
    "Tamandua": "Anteater",
    "Proechimys": "Spiny rat",
    "Leopardus": "Wild cat",
    "Equus": "Horse",
    "Columbina": "Dove",
    "Nyctidromus": "Goatsucker",
    "Ortalis": "Big bird",
    "Emballonura": "Bat",
    "Odontophorus": "Quail",
    "Geotrygon": "Quail dove",
    "Metachirus": "Mouse opossum",
    "Catharus": "Thrush",
    "Cerdocyon": "Fox",
    "Momotus": "Colorful bird",
    "Tapirus": "Tapir",
    "Canis": "Wolf",
    "Furnarius": "Ovenbird",
    "Didelphis": "Opossum",
    "Sylvilagus": "Cottontail",
    "Unknown": "Mystery",
}


def get_ClassNameMapSeedData():
    return [(k, definitions[k], v) for k, v in short_names.items()]
