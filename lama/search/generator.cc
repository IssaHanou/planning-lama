/*********************************************************************
 * Author: Malte Helmert (helmert@informatik.uni-freiburg.de)
 * (C) Copyright 2003-2004 Malte Helmert
 * Modified by: Silvia Richter (silvia.richter@nicta.com.au),
 *              Matthias Westphal (westpham@informatik.uni-freiburg.de)             
 * (C) Copyright 2008 NICTA and Matthias Westphal
 *
 * This file is part of LAMA.
 *
 * LAMA is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 3
 * of the license, or (at your option) any later version.
 *
 * LAMA is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 *********************************************************************/

#include "best_first_search.h"
#include "wa_star_search.h"
#include "ff_heuristic.h"
#include "globals.h"
#include "operator.h"
#include "landmarks_graph.h"
#include "landmarks_graph_rpg_sasp.h"
#include "landmarks_count_heuristic.h"

#include <cassert>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <sys/times.h>
#include <climits>

using namespace std;


int save_plan(const vector<const Operator *> &plan, const string& filename, int iteration);

int main(int argc, const char **argv) {
    struct tms start, search_start, search_end;
    struct tms landmarks_generation_start, landmarks_generation_end;
    times(&start);

    string landmark_filename = "tmp/landmarks.out";

    if(argc < 2 || argc > 3) {
	    std::cout << "Usage: \"search options [outputfile]\"\n";
    } else {
      landmark_filename = argv[2];
    }

    bool poly_time_method = false;
	cin >> poly_time_method;
    if(poly_time_method) {
		cout << "Poly-time method not implemented in this branch." << endl;
		cout << "Starting normal solver." << endl;
    }

    bool generate_landmarks = true;
    bool reasonable_orders = true;
    g_lgraph = NULL; 

	// Generate landmarks
    times(&landmarks_generation_start);
    read_everything(cin, generate_landmarks, reasonable_orders);
    times(&landmarks_generation_end);

	// Write landmarks to file
	g_lgraph->write(landmark_filename);

    int landmarks_generation_ms = (landmarks_generation_end.tms_utime -  landmarks_generation_start.tms_utime) * 10;
    if (g_lgraph != NULL) {
		cout << "Landmarks generation time: " << landmarks_generation_ms / 1000.0 << " seconds" << endl;
    }

    // Check whether landmarks were found, if not switch to FF-heuristic.
    if (generate_landmarks && g_lgraph->number_of_landmarks() == 0) {
		cout << "No landmarks found. This should only happen if task is unsolvable." << endl;
    }	
}
