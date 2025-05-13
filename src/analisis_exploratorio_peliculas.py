import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/imdb_1000.csv'
df = pd.read_csv(url)

# agregamos una nueva columna de la duracion en minutos
df["duration_hours"] = pd.to_datetime(df["duration"], unit="m")

# agrupamos las categorias y contamos los registros por categorias
df_genre = df.groupby("genre")["genre"].count()

# contamos cuantas categorias hay
amount_genre = df_genre.count()

# ordenamos el df por rating
df_sort_rating = df.sort_values("star_rating", ascending= False)
# guardamos las mejores 5 peliculas
top_peliculas = df_sort_rating[0:5]

df_sort_duration = df.sort_values("duration_hours", ascending= False)
# guardamos las mejores 5 peliculas
mayor_duration = df_sort_duration[0:5]


df.hist(bins=50)
plt.show()

