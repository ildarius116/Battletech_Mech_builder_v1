import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFont, ImageDraw
from textwrap import wrap
import webbrowser
from typing import Any, Dict, Callable

from comb_sum import best_combo  # Модуль расчета лучшей комбинации оружия
from localization import localization_dict as lang  # Модуль локализации пользовательского интерфейса (рус/англ)


class App(tk.Tk):
	""" Класс приложения """

	def __init__(self, loc=0):
		""" Конструктор окна приложения """
		tk.Tk.__init__(self)
		self.attributes('-topmost', False)  # поверх окон (True/False)
		#self.overrideredirect(False)  # рамка окна
		self.resizable(False, False)  # запрет растягивать
		self.title('Battletech Mech-builder')  # заголовок окна
		self.geometry("720x900+100+100")  # размеры окна
		self.search_dict = {}  # поисковый словарь
		self.search_list = []  # поисковый лист
		self.loc = loc  # язык интерфейса
		self.set_ui()

	def set_ui(self):
		""" Функция работы пользовательского интерфейса """

		# Настройки стиля интерфейса
		self.style = ttk.Style()
		self.style.theme_use("default")
		self.style.configure(self, width=15)  # расстояние между кнопками чекбокс

		# Размещение окна сервисных кнопок
		self.top_frm = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
		self.top_frm.pack(fill='both')
		self.style.configure(self.top_frm, width=300)

		# Размещение окна вывода результатов расчета
		self.frm_right = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
		self.frm_right.pack(side='right')
		canvas = tk.Canvas(self.frm_right, width=420, height=850)
		canvas.pack()

		def right_frame(text, result):
			""" Функция вывода текста над картинкой в окне результатов расчета """

			self.result_image = Image.open("Torso.png")
			font = ImageFont.truetype("arial.ttf", size=27, encoding="utf-8")
			if result:
				self.text_wraped = text
			else:
				self.text_wraped = "\n".join(wrap(text, 20))
			draw_text = ImageDraw.Draw(self.result_image)
			draw_text.text((5, 40), self.text_wraped, font=font, fill='lightgreen', align='left')
			self.photoImage = ImageTk.PhotoImage(self.result_image)
			self.lbl1 = tk.Label(canvas, image=self.photoImage)
			self.lbl1.pack(fill='both', side='top')
			self.lbl1.place(x=0, y=0)

		# Размещение окна под кнопку расчета
		self.frm_result = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
		self.frm_result.pack(fill='both', side='bottom')
		self.text = lang['Start'][self.loc]
		right_frame(self.text, False)

		# Размещение окна выбора свободного веса
		self.frm_weight = ttk.LabelFrame(self)
		self.frm_weight.pack(fill='both', side='top')
		self.lbl_weight = tk.Label(self.frm_weight, text=lang["Free Weight"][self.loc])
		self.lbl_weight.pack(side='left')
		self.style.configure(self.frm_weight, width=50)
		# Ползунок выбора значения свободного веса
		self.scale = ttk.Scale(self.frm_weight, from_=0, to=100, length=140, command=self.on_scale)
		self.scale.pack(side='right', padx=0)
		self.var_weight = tk.IntVar()
		self.lbl = ttk.Label(self.frm_weight, text=0, textvariable=self.var_weight)
		self.lbl.pack(side='right', padx=0)

		# Размещение окна под выбор собственного охлаждения Меха
		self.frm_cool = ttk.LabelFrame(self, text=lang['Own cooling'][self.loc])
		self.frm_cool.pack(fill='both', side='top', expand=True)
		self.chk_cool = ttk.LabelFrame(self.frm_cool, borderwidth=0)
		self.chk_cool.pack(side='left')

		# Размещение окна под прыжковые двигатели
		self.frm_jump = ttk.LabelFrame(self, text=lang['Jump Jets'][self.loc])
		self.frm_jump.pack(fill='both', side='top', expand=True)
		self.chk_jmp = ttk.LabelFrame(self.frm_jump, borderwidth=0)
		self.chk_jmp.pack(side='left')

		# Размещение окон под энергетическое вооружение
		self.frm_laser = ttk.LabelFrame(self, text=lang['Energy'][self.loc])
		self.frm_laser.pack(fill='both', side='top', expand=True)
		self.chk_lasers = ttk.LabelFrame(self.frm_laser, borderwidth=0)
		self.chk_lasers.pack(side='top')
		self.chk_m_lasers = ttk.LabelFrame(self.chk_lasers, borderwidth=0)
		self.chk_m_lasers.pack(side='left')
		self.chk_l_lasers = ttk.LabelFrame(self.chk_lasers, borderwidth=0)
		self.chk_l_lasers.pack(side='left')
		self.chk_ppc = ttk.LabelFrame(self.chk_lasers, borderwidth=0)
		self.chk_ppc.pack(side='right')
		self.combo_lasers = ttk.LabelFrame(self.frm_laser, borderwidth=0)
		self.combo_lasers.pack(side='top')

		# Размещение окон под баллистическое вооружение
		self.frm_cannon = ttk.LabelFrame(self, text=lang['Ballistic'][self.loc])
		self.frm_cannon.pack(fill='both', side='top', expand=True)
		self.chk_cannon = ttk.LabelFrame(self.frm_cannon, borderwidth=0)
		self.chk_cannon.pack(side='top')
		self.chk_cannon.configure(height=5, width=5)
		self.chk_acs = ttk.LabelFrame(self.chk_cannon, borderwidth=0)
		self.chk_acs.pack(side='left', anchor='n')
		self.chk_uacs = ttk.LabelFrame(self.chk_cannon, borderwidth=0)
		self.chk_uacs.pack(side='left', anchor='n')
		self.chk_lbxs = ttk.LabelFrame(self.chk_cannon, borderwidth=0)
		self.chk_lbxs.pack(side='right', anchor='n')
		self.combo_cannon = ttk.LabelFrame(self.frm_cannon, borderwidth=0)
		self.combo_cannon.pack(side='top', anchor='n')

		# Размещение окон под ракетное вооружение
		self.frm_missile = ttk.LabelFrame(self, text=lang['Missile'][self.loc])
		self.frm_missile.pack(fill='both', side='top', expand=True)
		self.chk_missile = ttk.LabelFrame(self.frm_missile, borderwidth=0)
		self.chk_missile.pack(side='top')
		self.chk_srms = ttk.LabelFrame(self.chk_missile, borderwidth=0)
		self.chk_srms.pack(side='left')
		self.chk_lrms_left = ttk.LabelFrame(self.chk_missile, borderwidth=0)
		self.chk_lrms_left.pack(side='left', anchor='n')
		self.chk_lrms_right = ttk.LabelFrame(self.chk_missile, borderwidth=0)
		self.chk_lrms_right.pack(side='left', anchor='n')
		self.combo_missile = ttk.LabelFrame(self.frm_missile, borderwidth=0)
		self.combo_missile.pack(side='top')

		# Размещение окон под вооружение поддержки
		self.frm_support = ttk.LabelFrame(self, text=lang['Support'][self.loc])
		self.frm_support.pack(fill='both', side='top', expand=True)
		self.chk_support = ttk.LabelFrame(self.frm_support, borderwidth=0)
		self.chk_support.pack(side='top')
		self.chk_mgs = ttk.LabelFrame(self.chk_support, borderwidth=0)
		self.chk_mgs.pack(side='left')
		self.chk_smalls = ttk.LabelFrame(self.chk_support, borderwidth=0)
		self.chk_smalls.pack(side='left')
		self.combo_support = ttk.LabelFrame(self.frm_support, borderwidth=0)
		self.combo_support.pack(side='top')

		# кнопки смены языка интерфейса
		btn_rus = ttk.Button(self.top_frm, text="Русский", command=self.app_rus)
		btn_rus.pack(side='left')
		btn_eng = ttk.Button(self.top_frm, text="English", command=self.app_eng)
		btn_eng.pack(side='left', padx=5, pady=5)

		# кнопка ON TOP
		self.var_on_top = tk.IntVar()
		chk_b_top = ttk.Checkbutton(self.top_frm, text=lang['ON TOP'][self.loc], variable=self.var_on_top, width=45,
		                            command=self.set_on_top)
		chk_b_top.pack(side='left', padx=50)

		# кнопки перехода на сайт Youtube
		self.image = ImageTk.PhotoImage(file="Youtube.png", size=10)
		btn_youtube = tk.Button(self.top_frm, image=self.image, text=lang['GUIDE'][self.loc],
		                        compound='left', width=150, font="arial.ttf", command=self.youtube)
		btn_youtube.pack(side='right', padx=5, pady=5)

		def combo_choice(outer_frame, weapon, mods, quantity, mydict):
			""" Функция обработки выбора раскрывающихся кнопок
				наполняет self.search_dict выбранным типом оружия, его/их модификацией(ми) и количеством.
				Пример: {Missiles {'mod': '++', 'quantity': '2'}, Ballistic {'mod': 'None', 'quantity': '2'}}
				"""
			def selected_quant(event):
				""" Функция обработки выбора количества оружия """
				for key, item in mydict.items():
					if key == weapon:
						item['quantity'] = combo_quant.get()

			def selected_mod(event):
				""" Функция обработки выбора модификации оружия """
				for key, item in mydict.items():
					if key == weapon:
						item['mod'] = combo_modify.get()

			if weapon == 'Jump Jets':
				mydict[weapon] = {'mod': jumps[0], 'quantity': '0'}
			else:
				mydict[weapon] = {'mod': mods[0], 'quantity': '0'}
			inner_frame = ttk.LabelFrame(outer_frame, borderwidth=0)
			inner_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
			combo_quant = ttk.Combobox(inner_frame, values=quantity, width=5, state='readonly')
			combo_quant.pack(side=tk.LEFT)
			combo_quant.current(0)
			combo_quant.bind("<<ComboboxSelected>>", selected_quant)
			combo_modify = ttk.Combobox(inner_frame, values=mods, width=10, state='readonly')
			combo_modify.current(0)
			combo_modify.pack(side=tk.LEFT)
			combo_modify.bind("<<ComboboxSelected>>", selected_mod)

		# все раскрывающиеся кнопки
		mods = ['None', '+', '++']
		jumps = ['Standard', 'Heavy', 'Assault']
		# jumps = [locals['Standard'][self.loc], locals['Heavy'][self.loc], locals['Assault'][self.loc]]
		quantity = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
		combo_choice(self.frm_jump, 'Jump Jets', jumps, quantity, self.search_dict)
		combo_choice(self.combo_cannon, 'Ballistic', mods, quantity, self.search_dict)
		combo_choice(self.combo_missile, 'Missile', mods, quantity, self.search_dict)
		combo_choice(self.combo_lasers, 'Energy', mods, quantity, self.search_dict)
		combo_choice(self.combo_support, 'Support', mods, quantity, self.search_dict)

		self.var_cool, self.var_jmp, self.var_warhmr, self.var_anni, \
			self.var_mg, self.var_s_laser, self.var_er_s_laser, self.var_s_p_laser, \
			self.var_ac_2, self.var_ac_5, self.var_ac_10, self.var_ac_20, self.var_gauss, \
			self.var_uac_2, self.var_uac_5, self.var_uac_10, self.var_uac_20, \
			self.var_lbx_2, self.var_lbx_5, self.var_lbx_10, self.var_lbx_20, \
			self.var_m_laser, self.var_er_m_laser, self.var_m_p_laser, \
			self.var_l_laser, self.var_er_l_laser, self.var_l_p_laser, \
			self.var_ppc, self.var_er_ppc, self.var_snub_ppc, self.var_srm_2, self.var_srm_4, self.var_srm_6, \
			self.var_lrm_5, self.var_lrm_10, self.var_lrm_15, self.var_lrm_20 = tk.IntVar(), tk.IntVar(), tk.IntVar(),\
			tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(),\
			tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), \
			tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), \
			tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar(), \
			tk.IntVar(), tk.IntVar()

		# список для хранения состояний выбора вооружения для поиска
		self.chk_list = [[self.var_cool, 'Own cooling', 'Own cooling'], [self.var_jmp, 'Jump Jets', 'Jump Jets'],
		                 [self.var_mg, 'MG', 'Support'], [self.var_s_laser, 'S Laser', 'Support'],
		                 [self.var_er_s_laser, 'ER S Laser', 'Support'], [self.var_s_p_laser, 'S P Laser', 'Support'],
		                 [self.var_ac_2, 'AC/2', 'Ballistic'], [self.var_ac_5, 'AC/5', 'Ballistic'],
		                 [self.var_ac_10, 'AC/10', 'Ballistic'], [self.var_ac_20, 'AC/20', 'Ballistic'],
		                 [self.var_uac_2, 'UAC/2', 'Ballistic'], [self.var_uac_5, 'UAC/5', 'Ballistic'],
		                 [self.var_uac_10, 'UAC/10', 'Ballistic'], [self.var_uac_20, 'UAC/20', 'Ballistic'],
		                 [self.var_lbx_2, 'LBX/2', 'Ballistic'], [self.var_lbx_5, 'LBX/5', 'Ballistic'],
		                 [self.var_lbx_10, 'LBX/10', 'Ballistic'], [self.var_lbx_20, 'LBX/20', 'Ballistic'],
		                 [self.var_gauss, 'Gauss Rifle', 'Ballistic'],
		                 [self.var_m_laser, 'M Laser', 'Energy'], [self.var_er_m_laser, 'ER M Laser', 'Energy'],
		                 [self.var_m_p_laser, 'M P Laser', 'Energy'],
		                 [self.var_l_laser, 'L Laser', 'Energy'], [self.var_er_l_laser, 'ER L Laser', 'Energy'],
		                 [self.var_l_p_laser, 'L P Laser', 'Energy'],
		                 [self.var_ppc, 'PPC', 'Energy'], [self.var_er_ppc, 'ER PPC', 'Energy'],
		                 [self.var_snub_ppc, 'Snub PPC', 'Energy'],
		                 [self.var_srm_2, 'SRM2', 'Missile'], [self.var_srm_4, 'SRM4', 'Missile'],
		                 [self.var_srm_6, 'SRM6', 'Missile'],
		                 [self.var_lrm_5, 'LRM5', 'Missile'], [self.var_lrm_10, 'LRM10', 'Missile'],
		                 [self.var_lrm_15, 'LRM15', 'Missile'], [self.var_lrm_20, 'LRM20', 'Missile']]

		# создание всех кнопок выбора вооружения для поиска
		chk_b_cool = ttk.Checkbutton(self.chk_cool, text=lang['60 Degrees'][self.loc], variable=self.var_cool, width=35)
		chk_b_cool.pack()
		chk_b_warhmr = ttk.Checkbutton(self.chk_cool, text=lang['Warhammer'][self.loc], variable=self.var_warhmr, width=35)
		chk_b_warhmr.pack()
		chk_b_anni = ttk.Checkbutton(self.chk_cool, text=lang['Annihilator'][self.loc], variable=self.var_anni, width=35)
		chk_b_anni.pack()
		chk_b_jmp = ttk.Checkbutton(self.chk_jmp, text=lang['Jump Jets'][self.loc], variable=self.var_jmp)
		chk_b_jmp.pack()
		chk_b_m_laser = ttk.Checkbutton(self.chk_m_lasers, text=lang['M Laser'][self.loc], variable=self.var_m_laser)
		chk_b_er_m_laser = ttk.Checkbutton(self.chk_m_lasers, text=lang['ER M Laser'][self.loc], variable=self.var_er_m_laser)
		chk_b_m_p_laser = ttk.Checkbutton(self.chk_m_lasers, text=lang['M P Laser'][self.loc], variable=self.var_m_p_laser)
		chk_b_l_laser = ttk.Checkbutton(self.chk_l_lasers, text=lang['L Laser'][self.loc], variable=self.var_l_laser)
		chk_b_er_l_laser = ttk.Checkbutton(self.chk_l_lasers, text=lang['ER L Laser'][self.loc], variable=self.var_er_l_laser)
		chk_b_l_p_laser = ttk.Checkbutton(self.chk_l_lasers, text=lang['L P Laser'][self.loc], variable=self.var_l_p_laser)
		chk_b_ppc = ttk.Checkbutton(self.chk_ppc, text=lang['PPC'][self.loc], variable=self.var_ppc)
		chk_b_er_ppc = ttk.Checkbutton(self.chk_ppc, text=lang['ER PPC'][self.loc], variable=self.var_er_ppc)
		chk_b_snub_ppc = ttk.Checkbutton(self.chk_ppc, text=lang['Snub PPC'][self.loc], variable=self.var_snub_ppc)
		chk_b_m_laser.pack(), chk_b_er_m_laser.pack(), chk_b_m_p_laser.pack()
		chk_b_l_laser.pack(), chk_b_er_l_laser.pack(), chk_b_l_p_laser.pack()
		chk_b_ppc.pack(), chk_b_er_ppc.pack(), chk_b_snub_ppc.pack()
		chk_b_ac_2 = ttk.Checkbutton(self.chk_acs, text=lang['AC/2'][self.loc], variable=self.var_ac_2)
		chk_b_ac_5 = ttk.Checkbutton(self.chk_acs, text=lang['AC/5'][self.loc], variable=self.var_ac_5)
		chk_b_ac_10 = ttk.Checkbutton(self.chk_acs, text=lang['AC/10'][self.loc], variable=self.var_ac_10)
		chk_b_ac_20 = ttk.Checkbutton(self.chk_acs, text=lang['AC/20'][self.loc], variable=self.var_ac_20)
		chk_b_uac_2 = ttk.Checkbutton(self.chk_uacs, text=lang['UAC/2'][self.loc], variable=self.var_uac_2)
		chk_b_uac_5 = ttk.Checkbutton(self.chk_uacs, text=lang['UAC/5'][self.loc], variable=self.var_uac_5)
		chk_b_uac_10 = ttk.Checkbutton(self.chk_uacs, text=lang['UAC/10'][self.loc], variable=self.var_uac_10)
		chk_b_uac_20 = ttk.Checkbutton(self.chk_uacs, text=lang['UAC/20'][self.loc], variable=self.var_uac_20)
		chk_b_lbx_2 = ttk.Checkbutton(self.chk_lbxs, text=lang['LBX/2'][self.loc], variable=self.var_lbx_2)
		chk_b_lbx_5 = ttk.Checkbutton(self.chk_lbxs, text=lang['LBX/5'][self.loc], variable=self.var_lbx_5)
		chk_b_lbx_10 = ttk.Checkbutton(self.chk_lbxs, text=lang['LBX/10'][self.loc], variable=self.var_lbx_10)
		chk_b_lbx_20 = ttk.Checkbutton(self.chk_lbxs, text=lang['LBX/20'][self.loc], variable=self.var_lbx_20)
		chk_b_gauss = ttk.Checkbutton(self.chk_acs, text=lang['Gauss Rifle'][self.loc], variable=self.var_gauss)
		chk_b_ac_2.pack(), chk_b_ac_5.pack(), chk_b_ac_10.pack(), chk_b_ac_20.pack()
		chk_b_uac_2.pack(), chk_b_uac_5.pack(), chk_b_uac_10.pack(), chk_b_uac_20.pack()
		chk_b_lbx_2.pack(), chk_b_lbx_5.pack(), chk_b_lbx_10.pack(), chk_b_lbx_20.pack()
		chk_b_gauss.pack()
		chk_b_srm_2 = ttk.Checkbutton(self.chk_srms, text=lang['SRM2'][self.loc], variable=self.var_srm_2)
		chk_b_srm_4 = ttk.Checkbutton(self.chk_srms, text=lang['SRM4'][self.loc], variable=self.var_srm_4)
		chk_b_srm_6 = ttk.Checkbutton(self.chk_srms, text=lang['SRM6'][self.loc], variable=self.var_srm_6)
		chk_b_lrm_5 = ttk.Checkbutton(self.chk_lrms_left, text=lang['LRM5'][self.loc], variable=self.var_lrm_5)
		chk_b_lrm_10 = ttk.Checkbutton(self.chk_lrms_left, text=lang['LRM10'][self.loc], variable=self.var_lrm_10)
		chk_b_lrm_15 = ttk.Checkbutton(self.chk_lrms_right, text=lang['LRM15'][self.loc], variable=self.var_lrm_15)
		chk_b_lrm_20 = ttk.Checkbutton(self.chk_lrms_right, text=lang['LRM20'][self.loc], variable=self.var_lrm_20)
		chk_b_srm_2.pack(), chk_b_srm_4.pack(), chk_b_srm_6.pack()
		chk_b_lrm_5.pack(), chk_b_lrm_10.pack(), chk_b_lrm_15.pack(), chk_b_lrm_20.pack()
		chk_b_mg = ttk.Checkbutton(self.chk_mgs, text=lang['MG'][self.loc], variable=self.var_mg)
		chk_b_s_laser = ttk.Checkbutton(self.chk_mgs, text=lang['S Laser'][self.loc], variable=self.var_s_laser)
		chk_b_er_s_laser = ttk.Checkbutton(self.chk_smalls, text=lang['ER S Laser'][self.loc], variable=self.var_er_s_laser)
		chk_b_s_p_laser = ttk.Checkbutton(self.chk_smalls, text=lang['S P Laser'][self.loc], variable=self.var_s_p_laser)
		chk_b_mg.pack(), chk_b_s_laser.pack(), chk_b_er_s_laser.pack(), chk_b_s_p_laser.pack()

		def get_list(my_dict):
			""" Функция преобразования поискового словаря self.search_dict в поисковый словарь формата:
			    search_list = [['Jump Jets', 'Light', '3'], ['S Laser', 'None', '4'],
			    ['SRM6', 'LRM10', 'LRM15', '++', '2'], ['M Lasers', 'L Lasers', '++', '0'],
			    ['AC/2', 'AC/20', 'UAC/5', 'LBX/10', 'None', '2']]
			 """
			self.search_list = []
			for key, value in my_dict.items():
				tmp_list = []
				for item in self.chk_list:
					if item[0].get() and item[2] == key:
						tmp_list.append(item[1])
				tmp_list.append(value['mod'])
				tmp_list.append(value['quantity'])
				self.search_list.append(tmp_list)

		def app_result(event):
			""" Функция обработки нажатия кнопки расчета """
			get_list(self.search_dict)

			tmp_boost = [0, 0]  # усиление для Энергетического и Баллистического оружия
			if self.var_warhmr.get():
				tmp_boost[0] = 1  # усиление для Энергетического оружия
			if self.var_anni.get():
				tmp_boost[1] = 1  # усиление для Баллистического оружия
			self.search_list.append(tmp_boost)

			if self.var_cool.get():  # выбор температуры собственного охлаждения меха
				self.search_list.append(60)
			else:
				self.search_list.append(30)

			weight = self.var_weight.get()  # получить значение свободного веса от ползунка
			self.search_list.append(int(weight))
			result = best_combo(self.search_list)   # получить результат расчетов
			result_frame(result)  # вывести на экран результат расчетов

		def result_frame(arg):
			""" Функция вывода результатов расчета на экран """
			if arg:
				txt = ''
				for key, value in arg.items():
					if key == 'Best weapons: ':
						txt += f'{lang[key][self.loc]} \n'
						for item in value:
							if item != ' ':
								txt += f'{lang[item][self.loc]} \n'
						txt += '\n'
					else:
						txt += f'{lang[key][self.loc]} = {str(int(value))} \n'
				right_frame(txt, True)
			else:
				txt = lang['Oops'][self.loc]
				right_frame(txt, False)

		# Кнопка расчета
		btn_result = ttk.Button(self.frm_result, text=lang['Calculation'][self.loc])
		btn_result.pack(side=tk.BOTTOM, fill=tk.BOTH)
		btn_result.bind('<Button-1>', app_result)

	def set_on_top(self):
		""" Функция обработки кнопки ON TOP """
		if self.var_on_top.get():
			self.attributes('-topmost', True)  # поверх окон
		else:
			self.attributes('-topmost', False)

	def on_scale(self, val):
		""" Функция обработки ползунка свободного веса """
		v = int(float(val))
		self.var_weight.set(v)

	def app_eng(self):
		""" Функция переключает язык интерфейса на английский """
		if self.loc:
			self.destroy()
			self.__init__(0)

	def app_rus(self):
		""" Функция переключает язык интерфейса на русский """
		if not self.loc:
			self.destroy()
			self.__init__(1)

	def youtube(self):
		""" Функция открывает youtube страницу """
		if not self.loc:  # GUIDE
			url = 'https://youtu.be/hhDE__W1zXY'
		else:  # Инструкция
			url = 'https://youtu.be/sLpUnjRptl8'
		webbrowser.open(url, new=1)


if __name__ == '__main__':
	root = App()
	root.mainloop()
