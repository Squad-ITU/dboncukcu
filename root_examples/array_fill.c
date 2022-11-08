#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TProfile.h"
#include "TRandom.h"
#include "TTree.h"

void array_fill(){
	
	TFile *f = new TFile ("create2.root","recreate");
	
	TTree *t1 = new TTree("t1","ornek 1");

	Float_t point[2];

	t1->Branch("point",&point,"point[2]/F");
	
	for (Int_t i = 0; i<1000; i++){
		
		point[0] = i;
		point[1] = i + 1000;
		t1->Fill();
	}

	t1 -> Print();
	f -> Write();
	f -> Close();

}
