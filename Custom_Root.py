import ROOT
import uproot
import numpy as np
import awkward as ak
import matplotlib.pyplot as plt

class Custom_Root:
    def __init__(self,root_path,tree_name):
        self.file = uproot.open(root_path+":"+tree_name)
        self.keys = self.file.keys()
    def __getitem__(self,key):
        return self.file[key].arrays()[key]
    def __call__(self):
        return self.file
    
    def plot_histogram(self,key,ax,
                       bins=50,range_info=(0,100),
                       histogram_labels={
                           "xlabel":"Muon $p_{\mathrm{T}}$ [GeV]",
                           "ylabel":"Number of muons / 1 GeV",
                           "title":"Transverse Momentum"
                       }):
        ax.hist(self.file[key], bins=100, range=range_info)
        ax.set_xlabel(histogram_labels["xlabel"])
        ax.set_ylabel(histogram_labels["ylabel"])
        ax.set_title(histogram_labels["title"])
        return ax
    
    def get_electron_muon(self):
        all_data=self.file.arrays([
            "Particle.PID",
            "Particle.Status",
            "Particle.Eta",
            "Particle.PT",
            "Particle.Phi"
        ], aliases={
            "Particle.PID":"pid",
            "Particle.Status":"status",
            "Particle.Eta":"eta",
            "Particle.PT":"pt",
            "Particle.Phi":"phi",
        },library="np")
        
        self.lepton_data = {
            "Electron":{
            "-":{"PT":[],"Eta":[],"Phi":[],"Event":[]},
            "+":{"PT":[],"Eta":[],"Phi":[],"Event":[]}
            },
            "Muon":{
            "-":{"PT":[],"Eta":[],"Phi":[],"Event":[]},
            "+":{"PT":[],"Eta":[],"Phi":[],"Event":[]}
            }
        }  
        num = len(all_data["Particle.PID"])
        for ev_i in range(num):
            electron_ind_positive=np.where(np.logical_and(all_data["Particle.PID"][ev_i]==11,all_data["Particle.Status"][ev_i]==1))[0]
            electron_ind_negative=np.where(np.logical_and(all_data["Particle.PID"][ev_i]==-11,all_data["Particle.Status"][ev_i]==1))[0]
            muon_ind_positive=np.where(np.logical_and(all_data["Particle.PID"][ev_i]==13,all_data["Particle.Status"][ev_i]==1))[0]  
            muon_ind_negative=np.where(np.logical_and(all_data["Particle.PID"][ev_i]==-13,all_data["Particle.Status"][ev_i]==1))[0]
            
            if len(electron_ind_positive)!=0:
                self.lepton_data["Electron"]["+"]["PT"]=np.append(self.lepton_data["Electron"]["+"]["PT"],all_data["Particle.PT"][ev_i][electron_ind_positive])
                self.lepton_data["Electron"]["+"]["Eta"]=np.append(self.lepton_data["Electron"]["+"]["Eta"],all_data["Particle.Eta"][ev_i][electron_ind_positive])
                self.lepton_data["Electron"]["+"]["Phi"]=np.append(self.lepton_data["Electron"]["+"]["Phi"],all_data["Particle.Phi"][ev_i][electron_ind_positive])
                self.lepton_data["Electron"]["+"]["Event"]=np.append(self.lepton_data["Electron"]["+"]["Event"],ev_i)
                
            if len(electron_ind_negative)!=0:
                self.lepton_data["Electron"]["-"]["PT"]=np.append(self.lepton_data["Electron"]["-"]["PT"],all_data["Particle.PT"][ev_i][electron_ind_negative])
                self.lepton_data["Electron"]["-"]["Eta"]=np.append(self.lepton_data["Electron"]["-"]["Eta"],all_data["Particle.Eta"][ev_i][electron_ind_negative])
                self.lepton_data["Electron"]["-"]["Phi"]=np.append(self.lepton_data["Electron"]["-"]["Phi"],all_data["Particle.Phi"][ev_i][electron_ind_negative])
                self.lepton_data["Electron"]["-"]["Event"]=np.append(self.lepton_data["Electron"]["-"]["Event"],ev_i)
                
            if len(muon_ind_positive)!=0:
                self.lepton_data["Muon"]["+"]["PT"]=np.append(self.lepton_data["Muon"]["+"]["PT"],all_data["Particle.PT"][ev_i][muon_ind_positive])
                self.lepton_data["Muon"]["+"]["Eta"]=np.append(self.lepton_data["Muon"]["+"]["Eta"],all_data["Particle.Eta"][ev_i][muon_ind_positive])
                self.lepton_data["Muon"]["+"]["Phi"]=np.append(self.lepton_data["Muon"]["+"]["Phi"],all_data["Particle.Phi"][ev_i][muon_ind_positive])
                self.lepton_data["Muon"]["+"]["Event"]=np.append(self.lepton_data["Muon"]["+"]["Event"],ev_i)
                
            if len(muon_ind_negative)!=0:
                self.lepton_data["Muon"]["-"]["PT"]=np.append(self.lepton_data["Muon"]["-"]["PT"],all_data["Particle.PT"][ev_i][muon_ind_negative])
                self.lepton_data["Muon"]["-"]["Eta"]=np.append(self.lepton_data["Muon"]["-"]["Eta"],all_data["Particle.Eta"][ev_i][muon_ind_negative])
                self.lepton_data["Muon"]["-"]["Phi"]=np.append(self.lepton_data["Muon"]["-"]["Phi"],all_data["Particle.Phi"][ev_i][muon_ind_negative])
                self.lepton_data["Muon"]["-"]["Event"]=np.append(self.lepton_data["Muon"]["-"]["Event"],ev_i)
        return self.lepton_data
        