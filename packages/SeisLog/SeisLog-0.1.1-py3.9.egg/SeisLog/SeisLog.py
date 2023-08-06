import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import lasio
from welly import Well
from segysak.segy import segy_loader

class prep_data:
    '''
    This class in the SeisLog package loads the well and depth seismic data in a format that allows
    all other classes to be properly exectued. It is recommended to use this class to load the data which
    includes the well deviation survey for each well.
    '''
    def __init__(self, well, dev_survey, seismic):   
        self.well_name=well
        self.seismic_volume=seismic
        
        # load well
        self.well = self.load_well(dev_survey)
        # load seismic
        self.seismic = self.load_seismic()

    def load_well(self,dev_survey):
        '''
        Load well and deviation survey using Welly
        '''
        self.well_data = Well.from_las(self.well_name)
        # Load deviation survey
        dev = np.loadtxt(dev_survey, skiprows=2, usecols = [0,1,2])
        # Add deviation to wells location attribute
        self.well_data.location.add_deviation(dev)
        # Add positioning (deltaX, deltaY, TVD_KB)
        self.position = np.loadtxt(dev_survey, skiprows=2, usecols = [4,5,3])
        self.position =  np.insert(self.position, 0, np.array((0, 0, 0)), 0)
        self.well_data.location.position=self.position
        return self.well_data

    def load_seismic(self):
        '''
        Load seismic survey using SegySak
        '''
        # load seismic data based on byte locations read from header
        # Based on header there is a scaler of 100 applied to the coordinates which must be reversed
        seis_data = segy_loader(self.seismic_volume, iline=189, xline=193, cdpx=181, cdpy=185, vert_domain='DEPTH')
        self.seis_data = seis_data.assign_coords(cdp_x=seis_data.cdp_x/100, cdp_y=seis_data.cdp_y/100)
        return self.seis_data
    

        
class trace_extraction:
    '''
    This class in the SeisLog package extracts the seismic trace and makes reelevant QC plots. 
    ITt used theeome a 'prepped' seismic volume
    along the wellpath of a 'prepped' well. 'Prepped' here refers to the fact that the data has been
    appropriately loaded for use in the SeisLog package. Please refer to class 'prep_data'.
    
    The class requires the well path, the prepped well and seismic output from the prep_data class, a min
    and max depth of extraction in TVDSS and the sampling interval of the depth seismic
    '''
    def __init__(self, well, prepped_well, prepped_seis, min_depth, max_depth, samp):
        
        self.well = well
        self.prep_well = prepped_well
        self.prep_seis = prepped_seis
        
        # Reload well using lasio for the purposes of extracting the depth  
        self.well_lasio = lasio.read(self.well)
        self.well_df = self.well_lasio.df().reset_index()
        
        # Convert well MD depths to TVDSS to match seismic depth standard
        temp = self.prep_well.location.md2tvd(self.well_df.DEPT) # MDD to TVD
        self.well_df['DEPT'] = temp - self.well_lasio.header['Well']['ELEV'].value # TVD to TVDSS

        # From well header, identify well location
        self.UTM_E = self.well_lasio.sections['Well']['XCOORD'].value
        self.UTM_N = self.well_lasio.sections['Well']['YCOORD'].value
        
        # Define extraction points 
        self.extraction_points = self.define_extraction_points(min_depth, max_depth, samp)
        
        self.trace = pd.DataFrame(columns = ['TVDSS','Amplitude'])
        
        for i in range(len(self.extraction_points)):
            space = self.prep_seis.seis.xysel(cdp_x=self.extraction_points[0][i],cdp_y=self.extraction_points[1][i])
            dep = self.extraction_points[2][i]*-1
            depth = space.sel(depth = self.extraction_points[2][i]*-1 )
            value = depth.data.values[0]
            self.trace.loc[i] = [dep]+[value]

    def define_extraction_points(self, min_depth, max_depth, samp):
        '''
        Extract seismic trace amplitudes along wellbore path
        '''
        # Extract depth values along well path
        extraction_points = self.prep_well.location.trajectory(datum=[self.UTM_E,self.UTM_N,self.well_lasio.header['Well']['ELEV'].value],elev=True)
        # Limit extraction points between user defined min and max depths
        extraction_points = extraction_points[-extraction_points[:,2] >= min_depth]
        extraction_points = extraction_points[-extraction_points[:,2] <= max_depth]
        # Round depth extraction values to the sampling of the depth seismic
        extraction_points[:,2] = np.round(extraction_points[:,2]/samp)*samp

        # Build data frame of extraction points
        df = pd.DataFrame(extraction_points)
        extraction_points = df.drop_duplicates(subset=[2], keep='first')
        extraction_points = extraction_points.reset_index()
        
        return extraction_points
    
    def plot_map(self):
        '''
        Plot a map view of the wellbore path within the seismic survey outline
        '''
        fig = plt.figure(figsize=(8, 8))
        
        # Plot seismic survey outline
        self.prep_seis.seis.plot_bounds(ax=plt.gca())
        plt.gca().set_aspect('equal', 'box')
        plt.gca().plot(np.array([self.UTM_E]), np.array([self.UTM_N]), "ok", label=f"Location of Well {self.well}")

        # Plot wellbore path  in X-Y
        well_path = self.prep_well.location.trajectory(datum=[self.UTM_E,self.UTM_N,self.well_lasio.header['Well']['ELEV'].value],elev=True)
        df = pd.DataFrame(well_path)
        plt.plot(df[0].values, df[1].values, 'k', label  = 'Well Path')
        plt.legend()

        txt=f"Location of Well {self.well} and deviated path\nrelative to 3D seismic data coverage (dotted line)."
        plt.figtext(0.5, 0.83, txt, wrap=True, horizontalalignment='center', fontsize=14, fontweight='bold');
        
    def plot_trace(self):
        '''
        Plot a log display of the extracted seismic trace amplitudes
        '''
        self.trace.plot(x='Amplitude', y='TVDSS', kind="line", figsize=(2,12), legend=False, title = f'Trace extracted along\n{self.well}')
        plt.gca().invert_yaxis()