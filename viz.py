#%%
import pandas as pd
import geopandas as gpd

import matplotlib.pyplot as plt

#%%

df = pd.read_stata('data/tables/gathered_estimates.dta')
print(df.shape)

#%%
# mexico states outline
states = gpd.read_file('data/shp/states/mexstates.shp')

# rural and urban areas
urban = gpd.read_file('data/shp/Mexico AGEB shapefiles_new/mexico_urban_agebs.shp')
rural = gpd.read_file('data/shp/Mexico AGEB shapefiles_new/mexico_rural_agebs.shp')

#%%

# keeping only the cols needed for joining to .dta
rural = rural[['concat_id', 'ent_mun', 'geometry']]
urban = urban[['concat_id', 'ent_mun', 'geometry']]

# placing them vertically on one another
combined=pd.concat([rural,urban], axis=0)
del(rural,urban)

#%%
# joining the dta to retain geometries
combined = pd.merge(combined, df, on='ent_mun', how='inner')
print(combined.shape)
del(df)

#%%

combined['fgt0_emdi_natdefl_resids'] = combined['fgt0_emdi_natdefl'] - combined['fgt0_con']
combined['fgt0_trnat_resids'] = combined['fgt0_trnat'] - combined['fgt0_con']
combined['fgt0_di1_resids'] = combined['fgt0_di1'] - combined['fgt0_con']

#%%

fig, ax = plt.subplots(1, 1)

# creates choropleth map
ax = combined.plot(column='fgt0_con', ax=ax, legend=True,figsize=[25,20],markersize=5,
                   legend_kwds={'label': "Estimate",'orientation': "horizontal"}, vmin=0,vmax=1)

# creates outline of mexico states on top
ax = states.plot(ax=ax,color='none', edgecolor='black', figsize=[25,20],markersize=25)
fig.set_size_inches(25,20)

ax.set_axis_off()
ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

ax.set_title('Headcount Poverty Benchmark (CONEVAL)', fontsize= 25)
fig.set_size_inches(25,20)

plt.savefig('output/images/combined-fgt0_con.png', bbox_inches="tight", pad_inches=0)

#%%

fig, ax = plt.subplots(1, 1)

ax = combined.plot(column='fgt0_di1', ax=ax, legend=True,figsize=[25,20],markersize=5,
                   legend_kwds={'label': "Direct Estimate",'orientation': "horizontal"}, vmin=0,vmax=1)

ax = states.plot(ax=ax,color='none', edgecolor='black', figsize=[25,20],markersize=25)
fig.set_size_inches(25,20)

ax.set_axis_off()

ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

ax.set_title('Headcount Poverty Direct Estimates', fontsize= 25)
fig.set_size_inches(25,20)


plt.savefig('output/images/combined-fgt0_di1.png', bbox_inches="tight", pad_inches=0)

#%%

combined['fgt0_di1_resids'].describe()

fig, ax = plt.subplots(1, 1)

# can change vmin and vmax here for resids but not entirely because might change appearance of actual performance
# kept numbers close to actual performance for now
ax = combined.plot(column='fgt0_di1_resids', ax=ax, legend=True,figsize=[25,20],markersize=5, cmap='magma',
                   legend_kwds={'label': "Direct Estimate Residuals",'orientation': "horizontal"}, vmin=-.5,vmax=.6)

ax = states.plot(ax=ax,color='none', edgecolor='black', figsize=[25,20],markersize=25)

fig.set_size_inches(25,20)

ax.set_axis_off()

ax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)

ax.set_title('Residuals: Headcount Poverty Direct  - Benchmark', fontsize= 25)
fig.set_size_inches(25,20)

plt.savefig('output/images/combined-fgt0_di1_resids.png', bbox_inches="tight", pad_inches=0)
