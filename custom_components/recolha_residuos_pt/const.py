"""Constants for Recolha de Resíduos Portugal."""

from __future__ import annotations

DOMAIN = "recolha_residuos_pt"
PLATFORMS = ["sensor", "calendar"]

CONF_MUNICIPALITY = "municipality"
CONF_LOCALITY = "locality"
CONF_OPERATOR = "operator"
CONF_SCHEDULES = "schedules"

WEEKDAYS = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}

WEEKDAY_LABELS = {
    "mon": "Segunda-feira",
    "tue": "Terça-feira",
    "wed": "Quarta-feira",
    "thu": "Quinta-feira",
    "fri": "Sexta-feira",
    "sat": "Sábado",
    "sun": "Domingo",
}

OPERATORS = {
    "other": "Outro / Município",
    "valorsul": "Valorsul",
    "simar": "SIMAR Loures e Odivelas",
    "amarsul": "Amarsul",
    "lipor": "LIPOR",
    "suldouro": "Suldouro",
    "ersuc": "ERSUC",
    "porto_ambiente": "Porto Ambiente",
}

WASTE_STREAMS = {
    "yellow": {
        "name": "Amarelo — Plástico e Metal",
        "short_name": "Amarelo",
        "color": "Amarelo",
        "hex": "#FDD835",
        "icon": "mdi:recycle",
        "material": "Embalagens de plástico, metal e pacotes de bebida",
        "put": [
            "Garrafas e frascos de plástico",
            "Embalagens de plástico",
            "Latas de bebidas e conservas",
            "Aerossóis vazios",
            "Pacotes de leite, sumo e outras embalagens de cartão para líquidos",
            "Sacos e películas de plástico",
        ],
        "avoid": [
            "Brinquedos e outros objetos de plástico que não sejam embalagens",
            "Eletrodomésticos",
            "Pilhas e baterias",
            "Embalagens com produtos perigosos",
        ],
    },
    "blue": {
        "name": "Azul — Papel e Cartão",
        "short_name": "Azul",
        "color": "Azul",
        "hex": "#1E88E5",
        "icon": "mdi:package-variant",
        "material": "Papel e cartão",
        "put": [
            "Jornais e revistas",
            "Papel de escrita e impressão",
            "Caixas de cartão espalmadas",
            "Sacos de papel",
        ],
        "avoid": [
            "Papel e cartão sujos de gordura",
            "Papel de cozinha e guardanapos sujos",
            "Fraldas e toalhetes",
            "Papel plastificado ou autocolante",
        ],
    },
    "green": {
        "name": "Verde — Vidro",
        "short_name": "Verde",
        "color": "Verde",
        "hex": "#43A047",
        "icon": "mdi:bottle-wine",
        "material": "Embalagens de vidro",
        "put": [
            "Garrafas de vidro",
            "Frascos e boiões de vidro",
        ],
        "avoid": [
            "Copos e loiça",
            "Cerâmica e porcelana",
            "Espelhos e vidros de janelas",
            "Lâmpadas",
        ],
    },
    "brown": {
        "name": "Castanho — Biorresíduos",
        "short_name": "Castanho",
        "color": "Castanho",
        "hex": "#795548",
        "icon": "mdi:food-apple",
        "material": "Biorresíduos / resíduos alimentares e orgânicos",
        "put": [
            "Restos de fruta e legumes",
            "Restos de refeições sem embalagem",
            "Borras de café e saquetas de chá sem agrafos",
            "Cascas de ovos",
        ],
        "avoid": [
            "Embalagens",
            "Vidro, metal ou plástico",
            "Fraldas e produtos de higiene",
            "Resíduos perigosos",
        ],
    },
    "residual": {
        "name": "Indiferenciado — Lixo comum",
        "short_name": "Indiferenciado",
        "color": "Cinzento/Preto",
        "hex": "#616161",
        "icon": "mdi:trash-can",
        "material": "Resíduos indiferenciados que não têm recolha seletiva adequada",
        "put": [
            "Resíduos domésticos não recicláveis",
            "Fraldas e produtos de higiene",
            "Pequenos resíduos sem solução de reciclagem doméstica",
        ],
        "avoid": [
            "Embalagens recicláveis",
            "Papel e cartão limpos",
            "Vidro de embalagem",
            "Pilhas, baterias, medicamentos e resíduos perigosos",
        ],
    },
}
