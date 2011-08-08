# -*- coding: utf-8 -*-

import re


class Virtual_Normalize(object):
    
    def __init__(self):
        self.exceptions = set(["entrevue", "escalier", "escaliers", "esclave", "esclaves", "escrime", "escorte",
                        "escortes", "escorter", "escapade", "escapades", "escamotter", "escarmouche",
                        "escarmouches", "escabeau", "escabeaux", "escadre", "escadres", "escadrille",
                        "escadron", "escalade", "escalades", "escalader", "escale", "escales", "escalope",
                        "escamotable", "escamotage", "escamotages", "escarcelle", "escargot", "escargots",
                        "escarpé", "escapées", "escapés", "escarpée", "escarpin", "escarre", "escarres", 
                        "escient", "esclaffer", "esclandre", "esclavagisme", "esclavagiste", "esclavagistes",
                        "escompte", "escompter", "escrimer", "s'escrimer", "escrimeur", "escrimeurs",
                        "escroc", "escrocs", "escroquer", "escroquerie", "escroqueries", "reçois", "aperçois",
                        "déçois", "conçois", "perçois", "vois", "entrevois", "revois", "prévois", "pourvois", 
                        "dois", "assois", "sursois", "chois", "déchois", "bois", "crois", "bois", "autrefois", 
                        "fois", "lois", "trois", "reçoit", "aperçoit", "déçoit", "conçoit", "perçoit", 
                        "voit", "entrevoit", "revoit", "prévoit", "pourvoit", "doit", "assoit", "sursoit", 
                        "choit", "déchoit", "boit", "croit", "reçoient", "aperçoient", "voient", "entrevoient", 
                        "revoient", "prévoient", "pourvoient", "assoient", "sursoient", "choient", "déchoient", 
                        "croient", "envoient", "renvoient", "aboient", "nettoient", "renettoient", "emploient", 
                        "noient", "apitoient", "atermoient", "broient", "charroient", "chatoient", "convoient",
                        "corroient", "côtoient", "coudoient", "dénoient", "déploient", "dévoient", "festoient",
                        "flamboient", "foudroient", "larmoient", "octroient", "ondoient", "ploient", "redéploient", 
                        "réemploient", "remploient", "renvoient", "rougeoient", "rudoient", "fourvoient", 
                        "soudoient", "tournoient", "tutoient", "verdoient", "vouvoient"])
                        
    def normalize(self, word):            
        word = re.sub('estre', 'etre', word)
        word = re.sub('ostre', 'otre', word)
        word = re.sub('^estat', 'etat', word)
        word = re.sub('tost', 'tot', word)        
        word = re.sub('mesme$', 'meme', word)
        word = re.sub('mesmes$', 'memes', word)
        word = re.sub('tousjour', 'toujour', word)
        word = re.sub('^esl', 'el', word)
        word = re.sub('ast$', 'at', word)
        word = re.sub('ust$', 'ut', word)
        word = re.sub('ist$', 'it', word)
        word = re.sub('inst$', 'int', word)
        word = re.sub('aysn', 'ain', word)
        word = re.sub('oust', 'out', word)
        word = re.sub('esf', 'ef', word) # like autresfois : fairly sure
        word = re.sub('ost$', 'ot', word) 
        word = re.sub('osts$', 'ot', word) #like imposts    
        ## Subtract a c
        word = re.sub('aincte$', 'ainte', word)
        word = re.sub('poinct', 'point', word)
        ## Replace u with v
        word = re.sub('ceuo', 'cevo', word)    
        word = re.sub('iue', 'ive', word) # fairly sure
        word = re.sub('uiu', 'uiv', word) #like poursuiuit : are there any words in French with the pattern viu ?
        word = re.sub('ievr$', 'ieur', word)
        word = re.sub('ovr$', 'our', word)
        word = re.sub('ouue', 'ouve', word) 
        word = re.sub('ouua', 'ouva', word)
        ## Replace y with i
        word = re.sub('cy$', 'ci', word) # I'm fairly sure about this one (voicy, mercy)
        word = re.sub('gy$', 'gi', word) #like rougy
        word = re.sub('ty$', 'ti', word) # like sorty, party
        word = re.sub('sy$', 'si', word) # like ainsy or aussy
        word = re.sub('quoy', 'quoi', word)
        word = re.sub('suy', 'sui', word)
        word = re.sub('^ennuy', 'ennui', word) # Can we assume that the general rule is re.sub('uy$', 'ui', ' ?
        word = re.sub('luy', 'lui', word)
        word = re.sub('partys', 'partis', word)
        word = re.sub('ry$', 'ri', word) #like attendry
        word = re.sub('ay$', 'ai', word)    
        word = re.sub('^croye\b', 'crois', word)
        word = re.sub('^vraye', 'vrai', word)
        word = re.sub('^parmy', 'parmi', word)
        ## Replace oi', 'oy by ai
        word = re.sub('oy$', 'ai', word)        
        word = re.sub('nois', 'nais', word) # should check for exceptions
        word = re.sub('oib', 'aib', word) # should check for exceptions
        ## Individual cases
        word = re.sub('loix$', 'lois', word)
        word = re.sub('agens', 'agents', word) 
        word = re.sub('intelligens', 'intelligent', word)
        word = re.sub('^lettrez', 'lettres', word)
        word = re.sub('^regars', 'regards', word)
        word = re.sub('^routte', 'route', word)
        word = re.sub('droitte', 'droite', word)
        word = re.sub('^faubour', 'faubourg', word) # cannot restrict the rule to bour', 'bourg because of words like tambour 
        word = re.sub('^quiter', 'quitter', word)
        word = re.sub('^sergens', 'sergents', word)
        word = re.sub('^persone', 'personne', word)
        word = re.sub('dessu$', 'dessus', word)
        word = re.sub('^maintement', 'maintenant', word)
        word = re.sub('^seulle', 'seule', word)
        word = re.sub('^faitte', 'faite', word)
        word = re.sub('trouue', 'trouve', word)
        word = re.sub('^absens', 'absents', word)
        word = re.sub('^petis', 'petits', word)
        word = re.sub('^suitte', 'suite', word)
        word = re.sub('^tranquile', 'tranquille', word)
        word = re.sub('^colomne', 'colonne', word)
        word = re.sub('grans$', 'grands', word)
        word = re.sub('^effect\b', 'effet', word)
        word = re.sub('accens', 'accents', word)
        word = re.sub('^hermite', 'ermite', word)
        word = re.sub('^horison', 'horizon', word)
        word = re.sub('^soufle', 'souffle', word)
        word = re.sub('prens', 'prends', word)
        word = re.sub('temp$', 'temps', word)
        word = re.sub('^parolle', 'parole', word)
        word = re.sub('flame', 'flamme', word)
        word = re.sub('^espris', 'esprits', word) 
        word = re.sub('suject', 'sujet', word)
        word = re.sub('project$', 'projet', word)
        ## Random common patterns
        word = re.sub('ans$', 'ants', word) # may be a problem, have to check some more
        word = re.sub('^milio', 'millio', word)
        word = re.sub('^milie', 'millie', word)
        word = re.sub('^chapp', 'chap', word) # like chappelle, chappeau, chappitre
        word = re.sub('iene$', 'ienne', word) # like anciene, tiene, siene : but is it reliable ?        
        
        if word not in self.exceptions:
            word = re.sub('ict$', 'it', word)
            word = re.sub('^esc', 'ec', word)
            word = re.sub('euue', 'euve', word)
            word = re.sub('ois$', 'ais', word)
            word = re.sub('oit$', 'ait', word)
            word = re.sub('oient$', 'aient', word)   

        return word


