from bs4 import BeautifulSoup
import os
import math

soup = BeautifulSoup(open("_list_.xml"), "html.parser")

maps = soup.find_all('map')

def to_rel(coords, bottom_left, top_right):
	height = top_right[1] - bottom_left[1];
	width = top_right[0] - bottom_left[0];
	coords[0] = (coords[0] - bottom_left[0]) / width;
	coords[1] = 1-((coords[1] - bottom_left[1]) / height);
	return coords;
	
def parse_coords(node):
	string = str(node).split(" ")
	coords = [float(string[0]), float(string[1])]
	return coords;
	
def draw_spawn(node, output_file, img):
	spawn1 = parse_coords(node.text);
	spawn1 = to_rel(spawn1, bottom_left, top_right);
	spawn_size = 80 * (dimensions[0]/1000);
	spawn1_loc = [spawn1[0]*dimensions[0] - spawn_size/2, spawn1[1]*dimensions[1] - spawn_size/2];
	#draw spawn1
	os.popen("convert "+ img + " -resize " + str(spawn_size) + "x" + str(spawn_size) + " temp_spawn.png");
	os.popen("composite -geometry +" + str(spawn1_loc[0]) + "+" + str(spawn1_loc[1]) + " temp_spawn.png " + output_file + " " + output_file);

	
for map in maps:
	filename = map.find('name').text + ".xml"

	doc = BeautifulSoup(open(filename), "html.parser")
	bottom_left = parse_coords(doc.boundingbox.bottomleft.text)
	top_right = parse_coords(doc.boundingbox.upperright.text)
	height = top_right[1] - bottom_left[1];
	width = top_right[0] - bottom_left[0];

	input_file = "maps_png/" + map.find('name').text + ".png";
	dimensions = os.popen("identify " + input_file).read();
	dimensions = dimensions.split(" ")[2].split("x");
	dimensions = [int(dimensions[0]), int(dimensions[1])];
	
	cap_size = 100 * (dimensions[0]/height)
	
	if (doc.gameplaytypes.ctf and doc.gameplaytypes.ctf.teambasepositions):
		output_file = "output/"+map.ctf.text;

		#parse ctf
		base1 = parse_coords(doc.gameplaytypes.ctf.teambasepositions.team1.contents[1].text);
		base2 = parse_coords(doc.gameplaytypes.ctf.teambasepositions.team2.contents[1].text);
		base1 = to_rel(base1, bottom_left, top_right);
		base2 = to_rel(base2, bottom_left, top_right);

		cap_size1 = cap_size;
		if (doc.gameplaytypes.ctf.teambasepositions.team1.radius1):
			cap_size1 = 2 * float(doc.gameplaytypes.ctf.teambasepositions.team1.radius1.text) * (dimensions[0]/height)
		cap_size2 = cap_size;
		if (doc.gameplaytypes.ctf.teambasepositions.team2.radius1):
			cap_size2 = 2 * float(doc.gameplaytypes.ctf.teambasepositions.team2.radius1.text) * (dimensions[0]/height)

		base1_loc = [base1[0]*dimensions[0] - cap_size1/2, base1[1]*dimensions[1] - cap_size1/2];
		base2_loc = [base2[0]*dimensions[0] - cap_size2/2, base2[1]*dimensions[1] - cap_size2/2];		
			
		#draw cap1
		os.popen("convert green_cap.png -resize " + str(cap_size1) + "x" + str(cap_size1) + " temp.png");
		os.popen("composite -geometry +" + str(base1_loc[0]) + "+" + str(base1_loc[1]) + " temp.png " + input_file + " " + output_file);
		#draw cap2
		os.popen("convert red_cap.png -resize " + str(cap_size2) + "x" + str(cap_size2) + " temp.png");
		os.popen("composite -geometry +" + str(base2_loc[0]) + "+" + str(base2_loc[1]) + " temp.png " + output_file + " " + output_file);
		
		if (doc.gameplaytypes.ctf.teamspawnpoints):
			draw_spawn(doc.gameplaytypes.ctf.teamspawnpoints.team1.position, output_file, "green_start.png")
			draw_spawn(doc.gameplaytypes.ctf.teamspawnpoints.team2.position, output_file, "red_start.png")
			
		print "<option data-mapid='" + map.find('name').text +"_ctf' data-size='" + str(int(width)) + "x" + str(int(height)) + "' value='<%=static_host%>/maps/" + map.ctf.text + "'><%=l('" + map.en.text + "')%></option>"

	if (doc.gameplaytypes.domination):
		output_file = "output/"+map.domination.text;
		base = parse_coords(doc.gameplaytypes.domination.controlpoint.text);
		base = to_rel(base, bottom_left, top_right);

		cap_size1 = cap_size;
		if (doc.gameplaytypes.domination.radius):
			cap_size1 = 2 * float(doc.gameplaytypes.domination.radius.text) * (dimensions[0]/height)

		base_loc = [base[0]*dimensions[0] - cap_size1/2, base[1]*dimensions[1] - cap_size1/2];

			
		os.popen("convert encounter_cap.png -resize " + str(cap_size1) + "x" + str(cap_size1) + " temp.png");
		os.popen("composite -geometry +" + str(base_loc[0]) + "+" + str(base_loc[1]) + " temp.png " + input_file + " " + output_file);
		
		draw_spawn(doc.gameplaytypes.domination.teamspawnpoints.team1.position, output_file, "green_start.png")
		draw_spawn(doc.gameplaytypes.domination.teamspawnpoints.team2.position, output_file, "red_start.png")
		
		print "<option data-mapid='" + map.find('name').text +"_domination' data-size='" + str(int(width)) + "x" + str(int(height)) + "' value='<%=static_host%>/maps/" + map.domination.text + "'><%=l('" + map.en.text + "')%> (<%=l('Encounter')%>)</option>"

	if (doc.gameplaytypes.assault2):
		output_file = "output/"+map.assault2.text;
	
		#parse ctf
		base1 = parse_coords(doc.gameplaytypes.assault2.teambasepositions.team1.position1.text);
		base2 = parse_coords(doc.gameplaytypes.assault2.teambasepositions.team1.position2.text);
		base1 = to_rel(base1, bottom_left, top_right);
		base2 = to_rel(base2, bottom_left, top_right);
		
		cap_size1 = cap_size;
		if (doc.gameplaytypes.assault2.teambasepositions.team1.radius1):
			cap_size1 = 2 * float(doc.gameplaytypes.assault2.teambasepositions.team1.radius1.text) * (dimensions[0]/height)
		cap_size2 = cap_size;
		if (doc.gameplaytypes.assault2.teambasepositions.team1.radius2):
			cap_size2 = 2 * float(doc.gameplaytypes.assault2.teambasepositions.team1.radius2.text) * (dimensions[0]/height)
		
		base1_loc = [base1[0]*dimensions[0] - cap_size1/2, base1[1]*dimensions[1] - cap_size1/2];
		base2_loc = [base2[0]*dimensions[0] - cap_size2/2, base2[1]*dimensions[1] - cap_size2/2];		
		
		#draw cap1
		os.popen("convert green_cap.png -resize " + str(cap_size1) + "x" + str(cap_size1) + " temp.png");
		os.popen("composite -geometry +" + str(base1_loc[0]) + "+" + str(base1_loc[1]) + " temp.png " + input_file + " " + output_file);
		#draw cap2
		os.popen("convert green_cap2.png -resize " + str(cap_size2) + "x" + str(cap_size2) + " temp.png");
		os.popen("composite -geometry +" + str(base2_loc[0]) + "+" + str(base2_loc[1]) + " temp.png " + output_file + " " + output_file);
		
		if (doc.gameplaytypes.assault2.teamspawnpoints.team1.position):
			draw_spawn(doc.gameplaytypes.assault2.teamspawnpoints.team1.position, output_file, "green_start.png")
		if (doc.gameplaytypes.assault2.teamspawnpoints.team2.position):
			draw_spawn(doc.gameplaytypes.assault2.teamspawnpoints.team2.position, output_file, "red_start.png")
			
		print "<option data-mapid='" + map.find('name').text +"_assault2' data-size='" + str(int(width)) + "x" + str(int(height)) + "' value='<%=static_host%>/maps/" + map.assault2.text + "'><%=l('" + map.en.text + "')%> (<%=l('Attack/Defence')%>)</option>"
		
	if (doc.gameplaytypes.assault):
		output_file = "output/"+map.assault.text;
	
		base1 = parse_coords(doc.gameplaytypes.assault.teambasepositions.team1.contents[1].text);
		base1 = to_rel(base1, bottom_left, top_right);
		base1_loc = [base1[0]*dimensions[0] - cap_size/2, base1[1]*dimensions[1] - cap_size/2];

		#draw cap1
		os.popen("convert green_cap.png -resize " + str(cap_size) + "x" + str(cap_size) + " temp.png");
		os.popen("composite -geometry +" + str(base1_loc[0]) + "+" + str(base1_loc[1]) + " temp.png " + input_file + " " + output_file);

		for position in doc.gameplaytypes.assault.teamspawnpoints.team2.find_all('position'):
			draw_spawn(position, output_file, "red_start.png")
			
		print "<option data-mapid='" + map.find('name').text +"_assault' data-size='" + str(int(width)) + "x" + str(int(height)) + "' value='<%=static_host%>/maps/" + map.assault.text + "'><%=l('" + map.en.text + "')%> (<%=l('Assault')%>)</option>"


