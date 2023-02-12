#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <stdlib.h> 
#include <pthread.h>
#include <iostream>
#include <filesystem>
#include <thread>
#include <algorithm>

using namespace std;
namespace fs = std::filesystem;
void *  best_patch_finder(void  *number);
# define my_sizeof(type) ((char *)(&type+1)-(char*)(&type))

struct args {
    int start;
    int end;
};

int total = 0;
int saved_time = 0;

int res_patch_check = 4;
vector<vector<string>> patches_matrix;
vector<vector<string>> finansz;
vector<vector<string>> tempfin;
vector<vector<string>> target_patch_matrix;

vector<string> toadd;
vector<string> allIn;

//string** answer_data = (string**)calloc(72000, sizeof( "C:\\Users\\Zachary\\Desktop\\C collage\\Editcolorofimage\\cut_and_downscaled_money_patches.csv") * 4);
string** answer_data = (string**)calloc(72000, sizeof( "C:\\Users\\Zachary\\Desktop\\C collage\\Editcolorofimage\\computation\\cut_and_downscaled_money_patches.csv") * 4);

//int number_of_threads = 2;
int number_of_threads = std::thread::hardware_concurrency();
using std::filesystem::current_path;
int main(){
	filesystem::path directoryPath = current_path();
    string fname = directoryPath.generic_string();
	std::size_t found = fname.find("computation");
	if (found != std::string::npos){
		fname = fname.substr(1, found+11);
		fname = "C:/" + fname.substr(1, fname.size()) + "cut_and_downscaled_money_patches.csv";
	}
	else{
		
		fname =  fname + "/computation/cut_and_downscaled_money_patches.csv";
	}
	std::replace( fname.begin(), fname.end(), '/', '\\');

	vector<string> row;
	string line, word;
	fstream file(fname, ios::in);
	if (file.is_open())
	{
		while (getline(file, line))
		{
			row.clear();

			stringstream str(line);

			while (getline(str, word, ','))
				row.push_back(word);
			target_patch_matrix.push_back(row);
		}
	}
	else
		cout << "Could not open the file:cut_and_downscaled_money_patches ";
		cout << fname;
		cout << "\n";

	//string fname2 = "C:\\Users\\Zachary\\Desktop\\C collage\\Editcolorofimage\\computation\\downscaled_patches_data.csv";
    fname = directoryPath.generic_string();
	found = fname.find("computation");
	if (found != std::string::npos){
		cout << "THIS INCLUDES COMPUTATIN \n";
		fname = fname.substr(1, found+11);
		fname = "C:/" + fname.substr(1, fname.size()) + "downscaled_patches_data.csv";
	}
	else{
		
		fname =  fname + "/computation/downscaled_patches_data.csv";
	}
	std::replace( fname.begin(), fname.end(), '/', '\\');
	string fname2 = fname;
	
	vector<string> row2;
	string line2, word2;
	fstream file2(fname2, ios::in);
	if (file2.is_open())
	{
		while (getline(file2, line2))
		{
			row2.clear();

			stringstream str(line2);

			while (getline(str, word2, ','))
				row2.push_back(word2);
			patches_matrix.push_back(row2);
		}
	}
	else
		cout << "Could not open the file downscaled_patches_data: ";
		cout << fname2;
		cout << "\n";


	int target;
	int best_score = 1000000;
	string best_patch = "";
	std::ofstream myfile;
	
	int sum = 0;
	int x;
	ifstream inFile;


	fname = directoryPath.generic_string();
	found = fname.find("computation");
	if (found != std::string::npos){
		fname = fname.substr(1, found+11);
		fname = "C:/" + fname.substr(1, fname.size()) + "num_patches_height.csv";
	}
	else{
		
		fname = fname + "/computation/num_patches_height.csv";
	}
	std::replace( fname.begin(), fname.end(), '/', '\\');
	string num_patches_height = fname;
	inFile.open(num_patches_height);

	if (!inFile) {
		cout << "Unable to open num_patches_height.csv; ";
		cout << num_patches_height;
		cout << "\n";
		exit(1); // terminate with error
	}

	while (inFile >> x) {
		sum = sum + x;
	}

	inFile.close();


    

	int temp;
	int temp2;
	int temp3;
	int temp4;
	int temp5;
	int temp6 = 0;
	int temp7;

	pthread_t threads[number_of_threads];
	struct args arguments[number_of_threads];


	int quat = target_patch_matrix.size() /number_of_threads;
	int exxr = target_patch_matrix.size() % number_of_threads;
	for (int i = 0; i < number_of_threads; i++){
		if (i == number_of_threads -1){
			arguments[i] = {i * quat, (i + 1) * quat + exxr};
		}
		else{
			arguments[i] = {i * quat, (i + 1) * quat};
		}	
	}

	//Opens calculated_answer to read the answers allready calculated into finansz
	string fname21 = "C:\\Users\\Zachary\\Desktop\\collage Movie\\computation\\calculated_answer.csv";


	//Opens answer.csv to store the correct patches
	fname21 = directoryPath.generic_string();
	found = fname21.find("computation");
	if (found != std::string::npos){
		fname21 = fname21.substr(1, found+11);
		fname21 = "C:/" + fname21.substr(1, fname21.size()) + "calculated_answer.csv";
	}
	else{
		
		fname21 =  fname + "/computation/answer.csv";
	}
	std::replace( fname21.begin(), fname21.end(), '/', '\\');


	vector<string> row21;
	string line21, word21;
	fstream file21(fname21, ios::in);
	if (file21.is_open())
	{
		while (getline(file21, line21))
		{
			row21.clear();

			stringstream str(line21);

			while (getline(str, word21, ','))
				row21.push_back(word21);
			finansz.push_back(row21);
		}
	}
	else
		cout << "Could not open the file downscaled_patches_data: ";
		cout << fname21;
		cout << "\n";


	for (int i = 0; i < number_of_threads; i++){pthread_create(&threads[i], NULL, best_patch_finder,  &arguments[i]);}
	for (int i = 0; i < number_of_threads; i++){pthread_join(threads[i], NULL);}

	//Opens answer.csv to store the correct patches
	fname = directoryPath.generic_string();
	found = fname.find("computation");
	if (found != std::string::npos){
		fname = fname.substr(1, found+11);
		fname = "C:/" + fname.substr(1, fname.size()) + "answer.csv";
	}
	else{
		
		fname =  fname + "/computation/answer.csv";
	}
	std::replace( fname.begin(), fname.end(), '/', '\\');
	string answerFile = fname;
	myfile.open(answerFile);

	int z = 0;
	for (int i = 0; i < target_patch_matrix.size(); i++){
		string x_coords   = answer_data[i][0];
		string y_coords   = answer_data[i][1];
		string best_patch = answer_data[i][2];
		myfile << x_coords + "," + y_coords + "," + best_patch  +"\n";
		auto p = std::to_string(temp6);
		temp6 = temp6 + 1;
		z++;
	}
	myfile.close();



	//Opens calculated_answer.csv to save the calculations for later use
	fname = directoryPath.generic_string();
	found = fname.find("computation");
	if (found != std::string::npos){
		fname = fname.substr(1, found+11);
		fname = "C:/" + fname.substr(1, fname.size()) + "calculated_answer.csv";
	}
	else{
		
		fname =  fname + "/computation/calculated_answer.csv";
	}
	std::replace( fname.begin(), fname.end(), '/', '\\');
	answerFile = fname;
	myfile.open(answerFile);
	int total_occ = 0;

	
	//Counts how many of the same image division is repeated
	for (int i = 0; i < target_patch_matrix.size(); i++){
		total_occ = 0;
		
		for (int i2 = 0; i2 < target_patch_matrix.size(); i2++){
			if (answer_data[i][4] == answer_data[i2][4]){
				total_occ++;
			}
		}
		if (total_occ > 1){
			
			
			toadd.push_back(answer_data[i][2]  + "," + answer_data[i][4] + "\n");
		}
		
	}
	for (int i = 0; i < toadd.size(); i++){
		myfile << toadd[i];
	}

	printf("%5.2f%% has been saved \n", 100 * ((float)saved_time)/ (float)total);
	//If occourneces are greater than 1, it checks 
	



	myfile.close();




	return 0;
}



void *  best_patch_finder(void  *number){

	int start = ((struct args*)number) -> start;
	int end   = ((struct args*)number) -> end;

	int target;
	int temp5;
	int temp4;
	int sum;
	string best_patch;
	int best_score;
	//int v = target_patch_matrix.size();
	string target_patch = "";

	
	total = 0;
	saved_time = 0;

	for (int z = start; z < end ; z++) {
		total++;
		bool allready_calculated = false;
		string target_patch1 = "";
		int si = target_patch_matrix[z].size();
		for (int lcv = 2; lcv < si; lcv++ ){
			target_patch1 += target_patch_matrix[z][lcv];
		}


		//Checks through calculated_answer to see if we allready have a solution
		for(int loopR = 0; loopR < finansz.size(); loopR++){
			
			if(finansz[loopR][1] == target_patch1){
				allready_calculated = true;
				best_patch = finansz[loopR][0];
			}
		}
		
		//allready_calculated = false;

		if (allready_calculated){
			saved_time++;

			answer_data[z] = new string[5];
			answer_data[z][0] = target_patch_matrix[z][0];
			answer_data[z][1] = target_patch_matrix[z][1];
			answer_data[z][2] = best_patch;

			target_patch = "";
			int si = target_patch_matrix[z].size();
			for (int lcv = 2; lcv < si; lcv++ ){
				target_patch += target_patch_matrix[z][lcv];
			}
			answer_data[z][4] = target_patch;
		}
		else{



			best_score = 1000000;
			for (int i = 0; i < patches_matrix.size(); i++)
			{
				if (patches_matrix[i][1] == "square"){
					target = 0;
					for (int j = 3; j < (res_patch_check * res_patch_check)*3 + 2; j++) {
						target = target + abs(stoi(patches_matrix[i][j]) - stoi(target_patch_matrix[z][j]));
					}

					if (target < best_score) {
						best_score = target;
						best_patch = patches_matrix[i][0];
					}
				}
				if (patches_matrix[i][1] == "landscape") {
					target = 0;
					temp4 = z + sum;
					for (int j = 3; j < (res_patch_check * res_patch_check) * 3 + 2; j++) {
						target = target + abs(stoi(patches_matrix[i][j]) - stoi(target_patch_matrix[z][j]));
					}
					
					if (temp4 < target_patch_matrix.size()) {
						for (int j = 2; j < (res_patch_check * res_patch_check) * 3 + 2; j++) {
							temp5 = j + (res_patch_check * res_patch_check) * 3;
							target = target + abs(stoi(patches_matrix[i][temp5]) - stoi(target_patch_matrix[temp4][j]));
						}
					}
					else {
						target = target + 100000;

					}
					target = target / 2;
					if (target < best_score) {
						best_score = target;
						best_patch = patches_matrix[i][0];
					}

				}
				if (patches_matrix[i][1] == "portrait") {
					target = 0;
					for (int j = 3; j < (res_patch_check * res_patch_check) * 3 + 2; j++) {
						target = target + abs(stoi(patches_matrix[i][j]) - stoi(target_patch_matrix[z][j]));
					}
					temp4 = z + 1;
					if (temp4 < target_patch_matrix.size()) {
						for (int j = 2; j < (res_patch_check * res_patch_check) * 3 + 2; j++) {
							temp5 = j + (res_patch_check * res_patch_check) * 3;
							target = target + abs(stoi(patches_matrix[i][temp5]) - stoi(target_patch_matrix[temp4][j]));
						}
					}
					else {
						target = target + 10000000;
					}
					target = target / 2;
					if (target < best_score) {
						best_score = target;
						best_patch = patches_matrix[i][0];
					}
				}
			}


			answer_data[z] = new string[5];
			answer_data[z][0] = target_patch_matrix[z][0];
			answer_data[z][1] = target_patch_matrix[z][1];
			answer_data[z][2] = best_patch;
			answer_data[z][3] = to_string(best_score);

			target_patch = "";
			int si = target_patch_matrix[z].size();
			for (int lcv = 2; lcv < si; lcv++ ){
				target_patch += target_patch_matrix[z][lcv];
			}
			answer_data[z][4] = target_patch;


			

			}

			float size_of_chunk = target_patch_matrix.size() / number_of_threads;
			int size_of_chunk_int = target_patch_matrix.size() / number_of_threads;
			float through = 100 * ((z%size_of_chunk_int)/size_of_chunk);
			int thread_number = z/size_of_chunk_int ;
			int accuracy = 100 *  (48960-best_score)/48960;
			printf("%5.2f%% completed    square: %-6d    thread: %-2d    accuracy: %2d%%    image selected: %-20s passed: %s\n", through, z,thread_number, accuracy,best_patch.c_str() , allready_calculated ? "true" : "false"  );
			}
	
}

