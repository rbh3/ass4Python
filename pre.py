import tkMessageBox
import matplotlib.pyplot as plt
import pandas as pd
import plotly.plotly as py
from PIL import Image
from sklearn.cluster import KMeans


class model:
    # Constructor
    def __init__(self):
        pass

    # cleans the data
    def clean(self, path):

        # read Excel file
        df = pd.read_excel(path)
        if(df.empty or 'country' not in df.columns or 'year' not in df.columns or 'Generosity' not in df.columns or 'Social support' not in df.columns ):
            tkMessageBox.showerror("K Means Clustering", "Invalid Excel File!")
            return

        # Fill missing values
        for col in df.columns:
            if (df[col].dtypes == "object"):
                continue
            else:
                df[col].fillna(df[col].mean(), inplace=True)

        # Standardization
        for col in df.columns:
            if (df[col].dtypes == "float64"):
                df[col] = (df[col] - df[col].mean()) / df[col].std()

        # Group by country & remove Year column
        df = df.groupby('country').mean()
        df.index.name = 'country'
        del df['year']
        self.df=df
        tkMessageBox.showinfo("K Means Clustering", "Preprocessing completed successfully!")

    # Cluster the data
    def k_means(self, n_clusters, n_init):
        kmeans = KMeans(n_clusters, n_init=n_init).fit(self.df)
        clst = kmeans.predict(self.df)
        self.df['Cluster'] = clst

        # Scatter plot
        plt.scatter(x=self.df['Social support'], y=self.df['Generosity'], c=self.df['Cluster'])
        plt.xlabel("Social Support")
        plt.ylabel("Generosity")
        plt.title("Generosity depends on Social Support")
        plt.savefig("scatterPlot.png")
        im = Image.open("scatterPlot.png")
        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im.save('scatterPlot.gif')

        # Horopleth map
        self.df.reset_index(inplace=True)
        scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],\
               [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
        data = [dict(
            type='choropleth',
            colorscale=scl,
            autocolorscale=False,
            locations=self.df['country'],
            z=self.df['Cluster'].astype(float),
            locationmode='country names',
            text=self.df['country'],
            marker=dict(
                line=dict(
                    color='rgb(255,255,255)',
                    width=2
                )),
            colorbar=dict(
                title="Cluster")
        )]

        layout = dict(
            title='World Horopleth map',
            geo=dict(
                scope='world',
                projection=dict(type='Mercator'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'),
        )

        py.sign_in("rbh3", "dcQuz8CsD31dn37oW8CM")
        fig = dict(data=data, layout=layout)
        py.plot(fig, filename='d3-cloropleth-map',auto_open=False)
        py.image.save_as(fig, filename="map.png")
        im = Image.open("map.png")
        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE)
        im.save('map.gif')
