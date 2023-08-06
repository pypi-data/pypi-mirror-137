import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd

class Plots:
    def topic_coor_plot(self, 
                        a_i,
                        topic_names = None):
        
        if topic_names == None: 
            topic_names = [str(i) for i in range(a_i.shape[0])]
        
        a_i = pd.DataFrame(a_i, columns = ["coordinate_1", "coordinate_2"])
        a_i["topic_name"] = topic_names
        
        fig = px.scatter(a_i, x="coordinate_1", y="coordinate_2", color = "topic_name")
        fig.update_xaxes(range=[-np.max(np.abs(a_i.iloc[:,0:2]), axis=0)[0]-0.3, 
                                np.max(np.abs(a_i.iloc[:,0:2]), axis=0)[0]+0.3], 
                         #rangemode = "tozero",
                         zeroline=True, zerolinecolor="gray")
        fig.update_yaxes(range=[-np.max(np.abs(a_i.iloc[:,0:2]), axis=0)[1]-0.3, 
                                np.max(np.abs(a_i.iloc[:,0:2]), axis=0)[1]+0.3], 
                         #rangemode = "tozero",
                         zeroline=True, zerolinecolor="gray")
        fig.show()
        
        return self
    
    

    def topic_trajectory_plot(self, 
                              a_is,
                              topic_names = None):
        
        if topic_names == None: 
            topic_names = [str(i) for i in range(a_is[0].shape[0])]
        
        fig = go.Figure()

        for i in range(np.array(a_is).shape[1]):
            a_i = np.array(a_is)[:,i,:]
            
            fig.add_trace(go.Scatter(x=a_i[:,0], y=a_i[:,1],
                            mode='lines+markers',
                            name=topic_names[i]))

        a_i = a_is[0]

        fig.add_trace(go.Scatter(x=a_i[:,0], y=a_i[:,1],
                            mode='text',
                            text=topic_names,
                            textposition="top left",
                            name="Most percentile"))

        fig.update_xaxes(rangemode = "tozero", zeroline=True, zerolinecolor="gray")
        fig.update_yaxes(rangemode = "tozero", zeroline=True, zerolinecolor="gray")

        fig.show()
        
        return self
        


