from otree.api import * 
import random




doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class C(BaseConstants):
    NAME_IN_URL = 'trust'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 4
    # Initial amount allocated to each player
    ENDOWMENT = cu(50)
    MULTIPLIER = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=[cu(5 * i) for i in range(11)],  # Multiplos de 5 de 0 a 50
        label="¿Cuánto quieres enviar?",
        min=cu(0), max=C.ENDOWMENT,
        default=cu(0),
        doc="""Cantidad enviada por el First Mover (FM).""",
    )
    sent_back_amount = models.CurrencyField(
        label="¿Cuánto quieres devolver?",
        min=cu(0),
        doc="""Cantidad devuelta por el Second Mover (SM).""",
    )

class Player(BasePlayer):
    pass


# FUNCTIONS

def creating_session(self):
    self.group_randomly()
    for group in self.get_groups():
        players=group.get_players()
        players.reverse()
        group.set_players(players)
    
    for player in self.get_players():
        player.participant.vars['payoff_round'] = random.randint(1, C.NUM_ROUNDS)                  

def sent_back_amount_max(self):
        return self.sent_amount * (C.MULTIPLIER-1)

def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLIER - group.sent_back_amount

def after_all_players_arrive(group: Group):
    set_payoffs(group)
    current_round = group.subsession.round_number
    for p in group.get_players():
        payoff_round = p.participant.vars['payoff_round']
        if current_round == payoff_round:
            p.participant.payoff = p.payoff

# PAGES
class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Send(Page):
    """This page is only for P1
    P1 sends amount (all, some, or none) to P2
    This amount is tripled by experimenter,
    i.e if sent amount by P1 is 5, amount received by P2 is 15"""

    form_model = 'group'
    form_fields = ['sent_amount']
    timeout_seconds = 80

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.group.sent_amount = cu(0)


class SendBackWaitPage(WaitPage):
    body_text = "Esperando a que los otros participantes tomen una decisión."


class SendBack(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']
    timeout_seconds = 80

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        tripled_amount = group.sent_amount * C.MULTIPLIER
        return dict(tripled_amount=tripled_amount)
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.group.sent_back_amount = cu(0)

class ResultsWaitPage(WaitPage):
    body_text="Esperando a que los otros participantes tomen una decisión."
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount=group.sent_amount * C.MULTIPLIER)

class agradecimientos(Page):
    @staticmethod
    def is_displayed(player):
        # Solo se muestra en la última ronda
        return player.subsession.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player):
        payoff_round = player.participant.vars['payoff_round']
        final_payoff = player.in_round(payoff_round).payoff
        return {
            'final_payoff': final_payoff,
            'payoff_round': payoff_round
        }

page_sequence = [Introduction, Send, SendBackWaitPage, SendBack, ResultsWaitPage, Results,agradecimientos]