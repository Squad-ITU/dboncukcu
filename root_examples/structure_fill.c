#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TProfile.h"
#include "TRandom.h"
#include "TTree.h"

void structure_fill(){
	
	TFile *f = new TFile ("create1.root","recreate");
	
	TTree *t1 = new TTree("t1","ornek 1");

	typedef struct {
	        Float_t	x;
		Float_t y;
		Float_t z;
		Float_t t;
	} POINT;
	
	POINT point;
	
	t1->Branch("point",&point,"x:y:z:t");

	for (Int_t i = 0; i<1000; i++){
		
		point.x = i;
		point.y = i + 1000;
		point.z = i + 2000;
		point.t = i + 3000;
		t1->Fill();
	}

	t1 -> Print();
	f -> Write();
	f -> Close();

}
