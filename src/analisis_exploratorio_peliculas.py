import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

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

# ordenamos la peliculas con mayor duracion
mayor_duration = df_sort_duration[0:5]

# creamos un diagrama de caja y bigotes y comprobamos los valores atipicos
plt.figure(figsize=(10,6))
plt.subplot(1,2,1) # 1 fila, 2 columnas primer subplot
sns.boxplot(y=df["duration"])
plt.title("Box plots - Con Outliers")
plt.xlabel("Duracion")
plt.ylabel("Minutos")

Q3 = df["duration"].quantile(0.75)
Q1 = df["duration"].quantile(0.25)

# calculamos el rango intercuartilico (IQR)
iqr = Q3 - Q1

# umbrales superior e inferior
inferior = Q1 - (1.5 * iqr)
superior = Q3 + (1.5 * iqr)

# guardamos los valores atipicos 
outliers = df[(df["duration"] < inferior) | (df["duration"] > superior)]

#filtramos el df sin valores atipicos
df_sin_outliers = df[(df["duration"] >= inferior) & (df["duration"] <= superior)]

# Grafico despues de eliminar outliers
plt.subplot(1,2,2) # 1 fila, 2 columnas, 2 grafico
sns.boxplot(y=df_sin_outliers["duration"])
plt.title("Box Plots - Sin Outliers")
plt.xlabel("Duracion")
plt.ylabel("Minutos")
plt.tight_layout() # ajusta los subplots para evitar superposiciones

# creamos un diagrama de dispersion generado por la siguiente hipotesis:
# mayor duracion mejor rating
plt.figure(figsize=(10,6))
plt.subplot()
sns.scatterplot(x = df_sin_outliers["star_rating"], y = df_sin_outliers["duration"])
plt.title("Diagrama de dispercion")
plt.xlabel("Rating")
plt.ylabel("Duracion")

plt.show()

# agrupamos en un df los generos y sacamos el promedio de rating por cada genero
# y ordenamos el df agrapado para mostrar claramente que genero tiene un mejor rating
df_genre_rating = df.groupby("genre")["star_rating"].mean().sort_values(ascending=False)

df['actors_list'] = df['actors_list'].apply(ast.literal_eval) # convertimos las cademas a objetos tipo lista
df_exploded = df.explode('actors_list') # creamos un df con una fila por actor

actor_counts = df_exploded['actors_list'].value_counts() # contamos la cantidad de peliculas por actor

# analizamos el promedio de rating por actor
actor_rating = df_exploded.groupby('actors_list')['star_rating'].mean().sort_values(ascending=False)

# creamos un nuevo df con la cantidad de peliculas por actor y su promedio de rating, y renombramos las columas
actor_summary = df_exploded.groupby('actors_list').agg({
    'title': 'count',
    'star_rating': 'mean'
}).rename(columns={'title': 'movie_count', 'star_rating': 'avg_rating'})

# Filtrar actores con al menos 5 películas y ordenar por rating
top_actors = actor_summary[actor_summary['movie_count'] >= 5].sort_values(by='avg_rating', ascending=False)

'''
INSIGHTS

1. ordenando la data por rating de mayor a menor podemos decir con certeza que las peliculas
que tienen un mayor rating pertenecen a la categoria de crimen.

2. analizando los datos y eliminando los valores atipicos y creando un grafico de caja y bigote del rating y la duracion
llegamos a la conclusion que no tienen una relacion clara, es decir que una pelicula para tener mayor rating 
no necesariamente puede ser corta o larga.

3. analizando los generos, podemos definir que los generos que tienen mayores rating son: Western (8.255556), 
Film-Noir (8.033333), History (8.000000)

4. con respecto a los actores mas productivos podemos decir que los que tienen mayor rating no tienen no son los mas
productivos en cuanto a cantidad de peliculas, sin embargo los actores que tienen mas cantidad de peliculas 
tienen mayores probabilidad de tener mayor rating
'''
