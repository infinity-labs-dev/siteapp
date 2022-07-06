import sys
from django.conf import Settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
import haversine as hs

# folium - map intergration
import folium
from resource_tracking.models.fault_management import FaultManagement

# pyrebase - firebase integration
import pyrebase
config={
    "authDomain": "eventmanagementdatabase.firebaseapp.com",
    "storageBucket": "gs://infinityandroid-151bc.appspot.com",    
    "apiKey": "MGcMpUOevOtCbmcLpYRTdIGgKUDYvjBL3zbDQNe7",
    "messagingSenderId": "154765625214",
    "databaseURL": "https://infinityandroid-151bc-default-rtdb.firebaseio.com/",
    "projectId": "infinityandroid-151bc",
    "appId": "1:154765625214:android:ceb9a261f27456588f552f",
}
firebase=pyrebase.initialize_app(config)
auth =firebase.auth()
database=firebase.database()

class UserTracking(View):
    
    def get(self, request):
        # print(request.GET['ticket_id'])
        try:
            # params                
            ticket_id = request.GET['ticket_id']  
            ticket=FaultManagement.objects.get(id=ticket_id)
            # print('tickete ===*****', ticket)            
            user_id=ticket.user.id
            # print('user_id *****', user_id)
            site_id=ticket.site.id
            # print('site_id +++++', site_id)
            
            # static variables
            place_lat = []
            place_lng = []          
            final_result_list = []
            

            # -- firebase records --
            result_set=database.child(user_id).child(site_id).child(ticket_id).get().val()        
            # print('type == ', type(user))
            if(result_set):
                # print('result_set ==', result_set)
                for coordinates in result_set.values():
                    newObject = []
                    place_lat.append(coordinates["latitude"])
                    place_lng.append(coordinates["longitude"])
                    
                    # print("mode: ==", coordinates["mode"])
                    # print("lat: ==", coordinates["latitude"])
                    # print("long: ==", coordinates["longitude"])
                    # print("timestamp: ==", coordinates["timestamp"])
                    newObject.append(coordinates['mode'])
                    newObject.append(coordinates['latitude'])
                    newObject.append(coordinates['longitude'])
                    newObject.append(coordinates['timestamp'])
                    final_result_list.append(newObject)
                                        
                # print('place_lat', place_lat)
                # print('place_lng', place_lng)
                    
                # -- map --        
                map = folium.Map(width=1260, height=540, location=[place_lat[0], place_lng[0]], zoom_start=16)
                
                # place_lat = [18.5642, 18.6011, 18.5602, 18.5074]
                # place_lng = [73.7769, 73.7641, 73.8031, 73.8077]
                print("len(place_lng)===", len(place_lng))
                points = []
                for i in range(len(place_lat)):
                    points.append([place_lat[i], place_lng[i]])

                for index,lat in enumerate(place_lat):
                    if(index ==0):
                        folium.Marker([lat, 
                                place_lng[index]],
                                popup="",
                                icon = folium.Icon(color='red',icon='play')).add_to(map)    
                    elif (index ==len(place_lng)-1):
                        folium.Marker([lat, 
                                place_lng[index]],
                                popup="",
                                icon = folium.Icon(color='red',icon='stop')).add_to(map)
                    else:
                        folium.Marker([lat, 
                                place_lng[index]],
                                popup="",
                                icon = folium.Icon(color='red',icon='plus')).add_to(map)         
                    
                # folium.PolyLine(points, color='green').add_to(map)            
                map = map._repr_html_()        
                # !! map !!            
                
                context = {
                    'map': map,
                    'final_result_list':final_result_list,
                } 
                # print('context', context)       
                return render(request, "tracking.html", context)    
            else:
                final_result_list=[]
                map = folium.Map(width=1260, height=540, location=[20.5937, 78.9629], zoom_start=10)
                folium.Marker([20.5937, 78.9629], popup="India", icon = folium.Icon(color='red',icon='location')).add_to(map)
                context = {
                    'map': map,
                    'final_result_list':final_result_list,
                } 
                # print('context', context)       
                return render(request, "tracking.html", context)               
                            
        except Exception as e:
            print("%s - %s at line: %s" % (sys.exc_info()
            [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
            # pass
            
class TrackSummary(View):
    def get(self, request):
        # print(request.GET['ticket_id'])
        try:
            # params                
            ticket_id = request.GET['ticket_id']  
            ticket=FaultManagement.objects.get(id=ticket_id)
            # print('tickete ===*****', ticket)            
            user_id=ticket.user.id
            # print('user_id *****', user_id)
            site_id=ticket.site.id
            # print('site_id +++++', site_id)
            
            # static variables       
            final_result_list = []
            total_distance_traveled=0
            place_lat=[]
            place_lng=[]
            loc1=[]
            loc2=[]
            # print("type == ", location1)
            # loc1=(28.426846,77.088834)
            # loc2=(28.394231,77.050308)

            # -- firebase records --
            result_set=database.child(user_id).child(site_id).child(ticket_id).get().val()        
            # print('type == ', type(user))
            if(result_set):
                # print('result_set ==', result_set)
                for coordinates in result_set.values():
                    place_lat.append(coordinates["latitude"])
                    place_lng.append(coordinates["longitude"]) 
                    
                # i=0                
                point_distance_list=[0]
                summation_distance_list=[0]
                # point_distance_list.append(0)
                index=0
                # print(len(place_lat))
                summation_distance=0
                while(index < len(place_lat)-1):
                    # print("index===",index)
                    loc1=[]
                    loc2=[]
                    loc1.append(place_lat[index])
                    loc1.append(place_lng[index])
                    loc2.append(place_lat[index +1])
                    loc2.append(place_lng[index +1])
                    # print("loc1==",loc1)
                    # print("loc2==",loc2)
                    
                    index=index+1
                    total_distance_traveled = hs.haversine(loc1,loc2)
                    point_distance_list.append(total_distance_traveled)
                    summation_distance+=total_distance_traveled
                    summation_distance_list.append(summation_distance)
            
                # print("point_distance_list======",point_distance_list)
                # print("len==",len(point_distance_list))
                total_distance_traveled = str(round(sum(point_distance_list), 2))
                                
                # total_distance_traveled = hs.haversine(loc1,loc2)
                # total_distance_traveled = str(round(total_distance_traveled, 2))
                # print("total_distance_traveled ===", total_distance_traveled)            
                # print("len final_result_list",len(final_result_list))
                i=0
                for coordinates in result_set.values():
                    newObject = []                  
                    
                    newObject.append(coordinates['mode'])
                    newObject.append(round(coordinates['latitude'], 6))
                    newObject.append(round(coordinates['longitude'], 6))
                    newObject.append(coordinates['timestamp'])
                    newObject.append(round(point_distance_list[i], 3))
                    newObject.append(round(summation_distance_list[i],3))
                    # print("i==",i)
                    final_result_list.append(newObject)
                    i+=1
                
                # print("final_result_list ============", final_result_list)   
                context = {
                    'final_result_list':final_result_list,
                    'total_distance_traveled':total_distance_traveled
                } 
                # print('context', context)       
                return render(request, "table_tracking.html", context)    
            else:
                final_result_list=[]
                total_distance_traveled=0
                context = {
                    'final_result_list':final_result_list,
                    'total_distance_traveled':total_distance_traveled,
                } 
                # print('context', context)       
                return render(request, "table_tracking.html", context)               
                            
        except Exception as e:
            print("%s - %s at line: %s" % (sys.exc_info()
            [0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
            # pass        
        
        
