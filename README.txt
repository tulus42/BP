==== Inštalácia ====
Je potrebné nainštalovať knižnicu colorama, a to príkazom:
python -m pip install colorama


==== Spustenie ====
Terminál:
	príkazom: "python3 main.py"
Windows/IDE:
	spustiť main.py

**Parametre spúšťania sa menia priamo v súbore "main.py" na vyznačenom mieste**

***Poznámka: pre správne zobrazenie progress baru je potrebné dostatočne široké okno terminálu***


==== Obsah súborov ====
	- main.py
		- hlavá časť programu 
		- prepojenie s ostatnámi modulmi
		- algoritmus učenia 
		- zobrazenie štatistík
	- environment.py
		- vytvorenie tabuľky akcií, z ktorej sa pri výbere akcie vyberajú už len validné ťahy
	- minimax.py
		- obsahuje algoritmus minimax (nie je dokonalý, ale pri dôkladnejšom prepracovaní bol rapidne navýšený výpočetný čas)
	- progress_bar.py
		- progress bar v termináli
		- len za účelom sledovania priebehu učenia
	- timer.py
		- sledovanie času behu programu
		- real-time výpočet predpokladaného času behu programu

==== Použitie ====
	Všetky potrebné úpravy pre skúšanie funkčnosti by mali prebiehať v súbore "main.py"

	V súbore "main.py" je možné upravovať najmä (avšak nie len) hodnoty v takto označenej sekcií:
	# =========================================================== #
	# EDIT                                                        #
	# =========================================================== #

	Sekcia START OF TRAINING obsahuje algoritmus učenia. 
		V sekcií tréningu je pri výbere akcie malý doplnok oproti základnej verzií rozhodovania.
		Algoritmus po porovnaní s epsilonom ešte porovnáva, či je v Q-table použiteľná hodnota.
		Ak nie je, tak tiež vyberá akciu náhodne.
		To by malo zlepšiť počiatočný výber akcií, avšak porovnávanie s 0 v tomto prípade nie je veľmi účinné.
		Myslím si, že je to kvôli nesprávnemu nastaveniu hodnôt odmien.
		Ak tento doplnok pokladáte za hlúposť, je k nemu v komentári pripravená alternatíva - pôvodný výber priamo z Q-table

	V rámci priebehu hry (učenia) sú dôležité najme premenné:
		- agent1, agent2	- pozície agentov - hodnota 0-24 (matica 5x5 políčok)
		- mrx_real_pos		- pozícia zlodeja - nevstupuje priamo do učenia (agenti túto pozíciu nepoznajú)
							- mení sa vždy po výbere ťahu agentov (a vyhodnotení úspešnosti) - súbor "minimax.py"

		- mrx_last_seen_pos - posledná videná pozícia zlodeja
		- mrx_seen_ago 		- čas, kedy bol zlodej naposledy videný (0-2 -> 0 = práve je na políčku "mrx_last_seen_pos", 2 = na políčku "mrx_last_seen_pos" bol pred 2 ťahmi)
			- tieto 2 hodnoty sa počítajú z mrx_real_pos pri výbere ťahu zlodeja, predávajú sa agentom

		- state				- aktuálny stav vyjadrený jedným číslom vypočítaným z:
								agent1, agent2, mrx_last_seen_pos, mrx_seen_ago
		- next_state		- nasledujúci vybraný stav, upravuje sa 2x:
								- pri výbere ťahu agentov (zmení sa len hodnota ovplyvňujúca pozície agent1, agent2)
								- pri výbere ťahu zlodeja (hodnota sa získa z funckie "get_next_move")

	Po skončení učenia sa zobrazia štatistiky:
		1. Dĺžka hry - ukazuje, či sa hra postupným učením skracuje, čo by znamenalo úspech
		2. Odmena - ukazuje celkovú odmenu za danú hru
		3. Výber naučených akcií - ukazuje, koľkokrát za hru si agenti vyberú z naučených ťahov (vyššie spomínaný doplnok)
			- Nepodarilo sa mi dosiahnuť, aby si vyberali naučené hodnoty -> ako som spomínal, myslím, že pomôže správne nastavenie odmien.
