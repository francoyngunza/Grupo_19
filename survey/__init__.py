from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='¿Cúal es tu edad?', min=18, max=100)
    gender = models.StringField(
        choices=[['Masculino', 'Masculino'], ['Femenino', 'Femenino']],
        label='¿Cúal es tu género?',
        widget=widgets.RadioSelect,
    )
    estado = models.StringField(
        choices=[['Egresado', 'Egresado'], ['Estudiante', 'Estudiante']],
        label='¿Eres estudiante o egresado?',
        widget=widgets.RadioSelect,
    )
    Universidad = models.StringField(
        choices=[['UP', 'UP'], ['PUCP', 'PUCP'],["UDEP","UDEP"],["UNMSM","UNMSM"],["UPC","UPC",],
                ["ULIMA","ULIMA"],["UNTRM","UNTRM"],["ESAN","ESAN"],["UNPRG","UNPRG"]],
    )
    confianza = models.StringField(
        choices=[
            'Muy baja',
            'Baja',
            'Moderada',
            'Alta',
            'Muy alta'
        ],
        label='¿En qué medida confiaste en tu compañero durante el juego?'
    )
    reciprocidad = models.StringField(
        choices=[
            'Muy baja',
            'Baja',
            'Moderada',
            'Alta',
            'Muy alta'
        ],
        label='¿Cómo percibes la reciprocidad de tu compañero?'
    )
    estrategia = models.StringField(
        choices=[
            'Seleccione una opción',
            'Sí, tenía una estrategia específica en mente',
            'No, decidí en el momento'
        ],
        label='¿Tenías una estrategia específica en mente al enviar una cantidad de dinero a tu compañero?'
    )
    Mi_strategy = models.StringField(
        choices=[
            'Enviar una cantidad mínima de dinero', 'Enviar una cantidad moderada de dinero',
            'Enviar la cantidad máxima posible de dinero', 'No tenía estrategia'
        ],
        label='¿Cuál crees que fue tu estrategia durante el juego?'
    )
    expected_strategy = models.StringField(
        choices=[
            'Enviar una cantidad mínima de dinero', 'Enviar una cantidad moderada de dinero',
            'Enviar la cantidad máxima posible de dinero', 'No estoy seguro/a'
        ],
        label='¿Cuál crees que fue la estrategia más probable de tu compañero durante el juego?'
    )
    expected_reciprocity = models.StringField(
        choices=['La misma cantidad', 'Más de la cantidad enviada', 'Menos de la cantidad enviada'],
        label='¿Cuánto esperabas que tu compañero te devolviera de la cantidad que le enviaste?'
    )
    percepcion_juego = models.StringField(
        choices=[
            'Muy justo',
            'Justo',
            'Neutral',
            'Injusto',
            'Muy injusto'
        ],
        label='¿Qué tan justo crees que fue el juego en general?'
    )


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender',"estado"]

class Universidad(Page):
    form_model = 'player'
    form_fields = ["Universidad"]

class preguntas(Page):
    form_model = 'player'
    form_fields = ['confianza', 'reciprocidad', 'estrategia','Mi_strategy']

class preguntas1(Page):
    form_model = 'player'
    form_fields = ['expected_strategy','expected_reciprocity', 'percepcion_juego']

class agradecimientos(Page):
    pass



page_sequence = [Demographics, Universidad, preguntas,preguntas1, agradecimientos]
