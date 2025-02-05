import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mticker

pd.set_option('display.max_rows', 6)

MAP_FILE = 'data/world.gpkg'
DEFAULT_COLOR = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
BACKGROUND_COLOR = '#D3D3D3'
EDGE_COLOR = 'white'
COLOR_MAP = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

class CountriesVisitedMap():
    
    fig = None
    ax = None
    
    def __init__(self) -> None:
        gdf = gpd.read_file('data/world.gpkg')
        gdf = gdf[ gdf['name_long'] != 'Antarctica' ]
        self._gdf = gdf.to_crs(3857) # Changes map projection
        
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
    
    
    def _new_plot(self, figsize=(10,8)):
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.margins(0)
        self.ax.axis('off')
    
    
    def _plot_background(self, column:str='status', color=BACKGROUND_COLOR):
        """Will draw all the countries where column is NaN"""
        self._gdf[ self._gdf[column].isna()].plot(ax=self.ax, color=color, edgecolor='white', linewidth=0.4)
    
    
    def plot(self, color=DEFAULT_COLOR, edgecolor=EDGE_COLOR, background_color=BACKGROUND_COLOR):
        """Plot the map. All the countries are highlighted in the same color.

        Args:
            color (string, optional): Color countries are highlighted with (as recognized by matplotlib). Defaults to DEFAULT_COLOR.
            edgecolor (string, optional): Color of the borders between countries. Defaults to EDGE_COLOR.
            background_color (string, optional): Color countries not highlighted are displayed in. Defaults to BACKGROUND_COLOR.
        """
        self._new_plot()
        self._gdf[ ~self._gdf['status'].isna() ].plot(
            ax=self.ax,
            color=color,
            edgecolor=edgecolor,
            linewidth=0.4
        )
        self._plot_background(color=background_color)
        
        
    def plot_status(self, colors=COLOR_MAP, edgecolor=EDGE_COLOR, background_color=BACKGROUND_COLOR):
        """Plot the map with countries in different colors according to the status given to them.

        Args:
            colors (string, optional): Color recognized by matplotlib. Defaults to COLOR_MAP.
            edgecolor (string, optional): Color of the border between countries. Defaults to EDGE_COLOR.
            background_color (string, optional): Color countries not highlighted are displayed in. Defaults to BACKGROUND_COLOR.
        """
        self._new_plot()
        
        count_status = self._gdf['status'].nunique()
        
        self._gdf.plot(
            ax=self.ax,
            column='status',
            cmap=mcolors.ListedColormap(colors[:count_status]),
            legend=True,
            legend_kwds={'loc': 'lower left'},
            edgecolor=edgecolor,
            linewidth=0.4,
        )

        self._plot_background(color=background_color)
        
    def plot_timeline(self, cmap='autumn', edgecolor=EDGE_COLOR):
        self._new_plot()
        
        self._gdf.plot(
            ax=self.ax,
            column='year_visited',
            cmap=cmap,
            legend=True,
            edgecolor=edgecolor,
            linewidth=0.4,
            legend_kwds={
                'shrink': 0.5,
            },
        )
        
        # Force the colorbar to show only whole numbers (years)
        cbar = self.ax.get_figure().get_axes()[-1]
        cbar.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensure whole numbers
        
        self._plot_background(column='year_visited')
        
    

    # gdf.explore(color=gdf['color'], missing_kwds={'color': 'lightgrey'})
    # plt.savefig('sample.png', bbox_inches="tight", pad_inches=0, transparent=True)
        
    


