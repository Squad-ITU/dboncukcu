#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int textfile_to_root(char const *txt_path ,char const *branch_name = "Vector" ,char const *tree_name = "Vector_Tree"  ,char const *root_filepath = "fromtextfile.root", int vector_length = 4,char const * ayrac = " "){
// Kullanım : root 'textfile_to_root.c(" * INPUT/TXT/PATH","BRANCH_NAME","TREE_NAME","OUTPUT/ROOTFILE/PATH","VECTOR_LENGTH"," ")'
// Başında * olan argumanlar zorunlu diğerleri değildir.
      	
	if (vector_length <=0){ // Girilen vektör uzunluğu 0'dan büyük olmalı aksi halde -2 hata kodu dönücek.
	 printf("Girilen Vektör uzunluğu  uygun değildir !(%d >0). \n",vector_length);
	 return -2;
	} 
	FILE *fp; // Dosya Pointerı
	char *line = NULL; // Okunan Satır
	size_t len = 0;  // Satır Uzunluğu Pointerı
	ssize_t read; // Okuma kontrolü içi
	fp = fopen(txt_path, "r"); // Dosya Okunuyor
       	if (fp == NULL){ // Dosya mevcut değilse -1 hata kodu dönücek
		printf("Okunacak Veri Bulunamadı...\n");
		return -1;
	}
	Float_t data[vector_length]; // Root verileri için boş alan oluşturuluyor.
	TFile *rootfile = new TFile(root_filepath,"recreate"); // ROOT dosyası oluşturuluyor.
	TTree *tree = new TTree(tree_name,tree_name); // Tree Oluşturuluyor.
	
	char branch_conf[200]; // Branch için ayar stringi 
	sprintf(branch_conf,"%s[%d]/F",branch_name,vector_length);
	
	tree-> Branch(branch_name,&data,branch_conf); // String Oluşturuluyor.
	
	while ((read = getline(&line, &len, fp)) != -1) { // txt Dosyası satır satır okunuyor.
	
		printf("Satır Verisi: %s ==>",line); // Satır verisi ham haliyle yazdırılıyor.

		char *temp = strtok(line,"["); // Satır verisi [sayi1  sayi2  ...  sayiN] şablonuna uygun parçalanıyor.
		temp = strtok(NULL,"[");
		temp = strtok(temp,"]");
	
		// Veri okumaya hazır. İlk Eleman okunuyor.
		temp = strtok(temp,ayrac);
		printf("1. %s -",temp);
		data[0] = atof(temp); 
	
		for (Int_t i = 1; i < vector_length; i++ ){ // Diğer Elemanlar okunuyor.
			temp = strtok(NULL,ayrac);
			printf("*%d. %s -",i,temp);
			data[i] = atof(temp);
		}
		tree -> Fill(); // Tree'ye yazılıyor.
		printf("\n");
	}
	// Memory boşaltılıyor, dosyaya yazma işlemleri yapılıyor.
	free(line);
	tree -> Print();
 	rootfile -> Write();
 	rootfile -> Close();
	exit(EXIT_SUCCESS);

}
