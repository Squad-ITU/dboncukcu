import ROOT
import numpy
import pandas
import matplotlib.pyplot as plt



##a = get_particle_properties_data(df,properties_list=properties_list,verbose_print=0)
def get_particle_properties_data(df,charge_settings = True,verbose_print=False,**kwargs):
	if "properties_list" in kwargs:
		propertie_names = kwargs["properties_list"]
	elif "particle_name" in kwargs and "properties" in kwargs:
		particle_name = kwargs["particle_name"]
		properties = kawrgs["properties"]
		propertie_names = [particle_name+"." + i for i in properties] #özellik isimleri delphes root dosyasına göre hazırlanıyor
	else:
		return None
	
	
	propertie_data = df.AsNumpy(columns=propertie_names) #istenen özellikler çekiliyor
	data_df = pandas.DataFrame(propertie_data) #dataframe dönüşümü yapılıyor
	numberOfEntry = len(data_df.index) #toplam entry sayısı bulunuyor
	
	root_datas = {} #özellik dataları için boş dict oluşturuluyor
	
	for name in propertie_names: #boş dict'in keyleri dolduruluyor
		root_datas[name] = numpy.array([])
	
	for entry in range(numberOfEntry):
		if verbose_print:
			print(entry)
		if len(data_df[data_df.columns[0]].values[entry]) == 0:
			continue
		for name in root_datas.keys(): #ilgili özelliğin mevcut adımdaki değeri return dict'ine eklenir.
			temp_data = data_df[name].values[entry]
			
			root_datas[name] = numpy.append(root_datas[name],temp_data)
	return root_datas


##dileptons = get_dilepton_events(df,properties_list=properties_list,verbose_print=False)
def get_dilepton_events(df):
	propertie_data = df.AsNumpy(columns=["Particle.PID","Particle.PT","Particle.Eta","Particle.Phi"])
	data_df = pandas.DataFrame(propertie_data)
	lepton_pids = {
    "Electron":[11,-11],
    "Muon":[13,-13],
    "Tau":[15,-15,17,-17],
	}
	data = {
    "Electron":{
        "-":{"PT":[],"Eta":[],"Phi":[]},
        "+":{"PT":[],"Eta":[],"Phi":[]}
    },
    "Muon":{
        "-":{"PT":[],"Eta":[],"Phi":[]},
        "+":{"PT":[],"Eta":[],"Phi":[]}
    },
    "Tau":{
        "-":{"PT":[],"Eta":[],"Phi":[]},
        "+":{"PT":[],"Eta":[],"Phi":[]}
    },
	}
	for event in range(len(data_df)):
    
		event_pid = data_df["Particle.PID"][event]

		for par_order in range(len(event_pid)):

			par_pid = data_df["Particle.PID"][event][par_order]

			if par_pid in lepton_pids["Electron"]:

				if par_pid > 0:
					data["Electron"]["+"]["PT"].append(data_df["Particle.PT"][event][par_order])
					data["Electron"]["+"]["Eta"].append(data_df["Particle.Eta"][event][par_order])
					data["Electron"]["+"]["Phi"].append(data_df["Particle.Phi"][event][par_order])

				elif par_pid < 0:

					data["Electron"]["-"]["PT"].append(data_df["Particle.PT"][event][par_order])
					data["Electron"]["-"]["Eta"].append(data_df["Particle.Eta"][event][par_order])
					data["Electron"]["-"]["Phi"].append(data_df["Particle.Phi"][event][par_order])

			elif par_pid in lepton_pids["Muon"]:

				if par_pid > 0:
					data["Muon"]["+"]["PT"].append(data_df["Particle.PT"][event][par_order])
					data["Muon"]["+"]["Eta"].append(data_df["Particle.Eta"][event][par_order])
					data["Muon"]["+"]["Phi"].append(data_df["Particle.Phi"][event][par_order])

				elif par_pid < 0:

					data["Muon"]["-"]["PT"].append(data_df["Particle.PT"][event][par_order])
					data["Muon"]["-"]["Eta"].append(data_df["Particle.Eta"][event][par_order])
					data["Muon"]["-"]["Phi"].append(data_df["Particle.Phi"][event][par_order])

			elif par_pid in lepton_pids["Tau"]:

				if par_pid > 0:
					data["Tau"]["+"]["PT"] = data_df["Particle.PT"][event][par_order]
					data["Tau"]["+"]["Eta"] = data_df["Particle.Eta"][event][par_order]
					data["Tau"]["+"]["Phi"] = data_df["Particle.Phi"][event][par_order]

				elif par_pid < 0:

					data["Tau"]["-"]["PT"] = data_df["Particle.PT"][event][par_order]
					data["Tau"]["-"]["Eta"] = data_df["Particle.Eta"][event][par_order]
					data["Tau"]["-"]["Phi"] = data_df["Particle.Phi"][event][par_order]
	return data

def plot_histogram_from_data(ax,data,particle_name,propertie_name):
	neg_info = data[particle_name]["-"][propertie_name]
	pos_info = data[particle_name]["+"][propertie_name]
	n1, bins1, patches1 = ax.hist(neg_info, 50,alpha=0.5,density=True,label=particle_name+"-")
	n2, bins2, patches2 = ax.hist(pos_info, 50,alpha=0.5,density=True,label=particle_name+"+")
	ax.set_xlabel(propertie_name)
	ax.set_ylabel("Probability")
	ax.set_title("Histogram of "+propertie_name)
	ax.legend(loc='upper right')
	ax.grid(True)
	return ax

def plot_dilepton_histogram(ax,xlabel,particle_name,charge_info,property_info,hist_title=None,bins=None,ylabel="Probability",density_setting = True,alpha_setting = 0.5):
	neg_info = property_info[charge_info < 0]
	pos_info = property_info[charge_info > 0]
	if type(bins) == type(None):
		bins = numpy.linspace(property_info.min()-0.1,property_info.max()+0.1,50)
	if type(hist_title) == type(None):
		hist_title = "Histogram of " + xlabel
	
	n1, bins1, patches1 = ax.hist(neg_info, bins,alpha=alpha_setting,density=density_setting,label=particle_name+"-")
	n2, bins2, patches2 = ax.hist(pos_info, bins,alpha=alpha_setting,density=density_setting,label=particle_name+"+")
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(hist_title)
	ax.legend(loc='upper right')
	ax.grid(True)
	return ax

def plot_histogram(ax,xlabel,particle_name,property_info,hist_title=None,bins=None,ylabel="Probability",density_setting = True,alpha_setting = 0.5):
	if type(bins) == type(None):
		bins = numpy.linspace(property_info.min()-0.1,property_info.max()+0.1,50)
	if type(hist_title) == type(None):
		hist_title = "Histogram of " + xlabel
	
	n1, bins1, patches1 = ax.hist(property_info, bins,alpha=alpha_setting,density=density_setting,label=particle_name)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(hist_title)
	ax.legend(loc='upper right')
	ax.grid(True)
	return ax