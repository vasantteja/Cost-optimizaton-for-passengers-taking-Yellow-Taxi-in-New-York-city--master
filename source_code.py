from math import sin, cos, sqrt, atan2, radians
import csv

# approximate radius of earth in miles
R = 3959.0

with open('mapping.csv', 'w') as csvfile:
	fieldnames = ['pickup_longitude', 'pickup_latitude', 'pickup_station_longitude', 'pickup_station_latitude', 'drop_longitude', 'drop_latitude', 'drop_station_longitude', 'drop_station_latitude', 'pick_zone', 'drop_zone', 'distance1', 'distance2', 'total_amount']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	with open('input.csv', 'rb') as csvfile:
		points = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in points:
			min_distance1 = 0.5
			min_distance2 = 0.5
			pick_up = False
			drop_of = False
			point = row[0].split(',')
			output_row = {'pickup_longitude':point[2], 'pickup_latitude':point[3], 'pickup_station_longitude':"", 'pickup_station_latitude':"", 'drop_longitude':point[4], 'drop_latitude':point[5], 'drop_station_longitude':"", 'drop_station_latitude':"", 'pick_zone':"", 'drop_zone':"", 'distance1':"", 'distance2':"", 'total_amount':""}
			with open('stations.csv', 'rb') as csvfile:
				stationsList = csv.reader(csvfile, delimiter=' ', quotechar='|')
				for presentStation in stationsList:
					station = presentStation[0].split(',')
					
					lat1 = radians(float(station[1]))
					lon1 = radians(float(station[0]))
					
					# pickup calcalation
					lat2 = radians(float(point[3]))
					lon2 = radians(float(point[2]))

					dlon = lon2 - lon1
					dlat = lat2 - lat1

					a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
					c = 2 * atan2(sqrt(a), sqrt(1 - a))

					distance = R * c
					if distance < min_distance1:
						min_distance1 = distance
						output_row['pickup_station_latitude'] = station[0]
						output_row['pickup_station_longitude'] = station[1]
						output_row['distance1'] = distance
						output_row['pick_zone'] = station[2]
						pick_up = True


					# dropoff calculation
					lat2 = radians(float(point[5]))
					lon2 = radians(float(point[4]))

					dlon = lon2 - lon1
					dlat = lat2 - lat1

					a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
					c = 2 * atan2(sqrt(a), sqrt(1 - a))

					distance = R * c
					if distance < min_distance2:
						min_distance2 = distance
						output_row['drop_station_latitude'] = station[0]
						output_row['drop_station_longitude'] = station[1]
						output_row['distance2'] = distance
						output_row['drop_zone'] = station[2]
						drop_of = True

				if pick_up == True and drop_of == True:
					print point[7]
					output_row['total_amount'] = point[7]
				writer.writerow(output_row)
				# print("Result:", distance)