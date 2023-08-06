import h5py
import json 
import ast
from geojson import LineString, Point, Feature
from turfpy.measurement import point_to_line_distance
import geohash
import osmium as osm

class OsmRoads(osm.SimpleHandler):
    def __init__(self,hdf5_file_name:str,openstreetmap_pbf_file_name=None):
        osm.SimpleHandler.__init__(self)
        if openstreetmap_pbf_file_name!=None:
            self.hdf5_connection = self.__load_openstreetmap_road_data(openstreetmap_pbf_file_name,hdf5_file_name)
        else:
            self.hdf5_connection = self.__load_hdf5_file(hdf5_file_name)
    def __insert_geohash_road_segment(self, road_segment:dict):
        geohash_prefix=road_segment['geohash'][:6]
        geohash_suffix=road_segment['geohash'][6:]
        try:
            self.hdf5_connection.create_group(geohash_prefix)
        except:
            pass 
        try:
            group2=self.hdf5_connection.create_group(geohash_prefix+'/'+geohash_suffix)
        except:
            group2= self.hdf5_connection.get('/'+geohash_prefix+'/'+geohash_suffix)
        item_count=str(len(group2.items())+1)
        
        group2.create_dataset(item_count,data=json.dumps(road_segment).encode("utf-8"))
    def way(self, way):
       
            if way.tags.get("highway") in {'bridleway','construction','cycleway','footway','living_street','motorway','motorway_link','path','pedestrian','platform','primary','primary_link','proposed','raceway','residential','rest_area','road','secondary','secondary_link','service','steps','tertiary','tertiary_link','track','trunk','trunk_link','unclassified'}:
                #node.ref    
                nodes=[]
                for member_node in way.nodes:
                    if member_node.location.valid():
                        nodes.append([member_node.lon,member_node.lat])
                geohash_mid_point_index=int(len(nodes)/2)
                geohash_key=geohash.encode(nodes[geohash_mid_point_index][1],nodes[geohash_mid_point_index][0])
                way_points="["
                for point in nodes:
                    way_points+='['+str(point[0])+","+str(point[1])+'],'
                way_points=way_points[:-1]+"]"
                road_segment=dict(way.tags)
                road_segment['geohash']=geohash_key 
                road_segment['coordinates']=way_points
                self.__insert_geohash_road_segment(road_segment)
        
        
    def __load_openstreetmap_road_data(self,openstreetmap_pbf_file_name, hdf5_file_name):
        self.hdf5_connection=h5py.File(hdf5_file_name, "w")
        self.apply_file(openstreetmap_pbf_file_name,locations=True)
        self.hdf5_connection.close()
        ##return read only handler 
        return self.__load_hdf5_file(hdf5_file_name)
    def __load_hdf5_file(self,hdf5_file_name):
        try:
            return h5py.File(hdf5_file_name, "r")
        except: 
            raise ValueError("The program could not load the file.Possible invalid/corrupt file.")
    
    def get_closest_road(self,latitude:float, longitude:float):
        DISTANCE_MAX=1000
        geohash_prefix=geohash.encode(latitude,longitude)[:6]
        point=Feature(geometry=Point([longitude, latitude]))
        distance=DISTANCE_MAX
        road_information={}
        for road_segments in self.hdf5_connection[geohash_prefix]:
            for road_subsegments in self.hdf5_connection[geohash_prefix][road_segments].keys():
                metadata_dictionary=ast.literal_eval(self.hdf5_connection[geohash_prefix][road_segments][road_subsegments][()].decode("utf-8"))
                line_string=Feature(geometry=LineString(ast.literal_eval(metadata_dictionary['coordinates'])))
                current_distance=point_to_line_distance(point, line_string)
                if current_distance<distance:
                    distance=current_distance
                    road_information=metadata_dictionary
                    road_information['distance']=distance
        return road_information
    def close_database(self):
        try:
            self.hdf5_connection.close()
        except:
            pass 
    def __del__(self):
        self.hdf5_connection.close()