import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 6)

MAP_FILE = 'data/world.gpkg'
DEFAULT_COLOR = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
BACKGROUND_COLOR = '#D3D3D3'
EDGE_COLOR = 'white'

class CountriesVisitedMap():
    
    fig = None
    ax = None
    
    def __init__(self) -> None:
        gdf = gpd.read_file('data/world.gpkg')
        gdf = gdf[ gdf['name_long'] != 'Antarctica' ]
        self._gdf = gdf.to_crs(3857) # Changes projection
        
    def country_exists(self, country:str) -> bool:
        return True if country in list(self._gdf['name_long']) else False
    
    def add_country(self, country:str, year:int = 0, status:str='Visited'):
        if year != 0 and (year < 1900 or year > 2050):
            raise ValueError('Year needs to be between 1900 and 2050.')

        if not self.country_exists(country):
            raise ValueError(f'The country {country} doesn\'t exist.')
        
        self._gdf.loc[ self._gdf['name_long'] == country, 'status'] = status
        if year != 0:
            self._gdf.loc[ self._gdf['name_long'] == country, 'year_visited'] = year
            
    def add_country_visited(self, country:str, year:int = 0) -> None:
        self.add_country(country, year, status='Visited')
    
    def add_country_lived_in(self, country:str, year:int = 0) -> None:
        self.add_country(country, year, status='Lived in')
    
    def _new_plot(self, figsize=(10,8)):
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.axis('off')
        self.ax.margins(0)
    
    def _plot_background(self, column:str, color=BACKGROUND_COLOR):
        """Will draw all the countries where column is NaN"""
        self._gdf[ self._gdf['status'].isna()].plot(ax=self.ax, color=color, edgecolor='white', linewidth=0.4)
    
    def plot(self, color=DEFAULT_COLOR, edgecolor=EDGE_COLOR):
        self._new_plot()
        self._gdf[ ~self._gdf['status'].isna() ].plot(ax=self.ax, color=color, edgecolor=edgecolor, linewidth=0.4)
        self._plot_background('status')

    # gdf.explore(color=gdf['color'], missing_kwds={'color': 'lightgrey'})
    # plt.savefig('sample.png', bbox_inches="tight", pad_inches=0, transparent=True)
        
    


