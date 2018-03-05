from collections import namedtuple

# g1politica, folha_poder, EstadaoPolitica, UOLPolitica, OGloboPolitica
g1politica = 31504246
politica_estadao = 76369002
folha_poder = 90963197
uol_politica = 133435134
o_globo_politica = 156719729

Newswire = namedtuple("Newswire","name id")

g1 = Newswire("g1politica", 31504246)
estadao = Newswire("EstadaoPolitica", 76369002)
folha = Newswire("folha_poder", 90963197)
uol = Newswire("UOLPolitica", 133435134)
globo = Newswire("OGloboPolitica", 156719729)

newswire_ids = [g1politica, politica_estadao, folha_poder, uol_politica, o_globo_politica]
newswire_list = [g1, estadao, folha, uol, globo]