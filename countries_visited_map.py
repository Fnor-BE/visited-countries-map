import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', 6)

MAP_FILE = 'data/world.gpkg'
DEFAULT_COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]

class CountriesVisitedMap():
    
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
    
    def plot(self, color=DEFAULT_COLORS):
        fig = plt.figure(figsize=(10,8))
        ax = fig.add_axes([0, 0, 1, 1])

        self._gdf[ ~self._gdf['status'].isna() ].plot(ax=ax, color=color)
        ax.axis('off')
        ax.margins(0)

        # gdf.explore(color=gdf['color'], missing_kwds={'color': 'lightgrey'})
        self._gdf[ self._gdf['status'].isna()].plot(ax=ax, color='#D3D3D3', edgecolor='white', linewidth=0.4)
        # plt.savefig('sample.png', bbox_inches="tight", pad_inches=0, transparent=True)


