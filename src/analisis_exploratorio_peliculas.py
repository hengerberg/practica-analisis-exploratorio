import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://raw.githubusercontent.com/justmarkham/pandas-videos/master/data/imdb_1000.csv'
df = pd.read_csv(url)
print(df.head())
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

# con el metodo describe analizamos los posibles outliers que pueden haber
# en este caso observamos que en la columna duration si pueden existir anomalias
#print(df.describe())

# graficamos las columnas y decidimos analizar con mas profundidad la columna duration
#df.hist(bins=50)
#plt.show()

column_duration = df["duration"]

# creamos un diagrama de caja y bigotes y comprobamos los valores atipicos
plt.figure(figsize=(10,6))

plt.subplot(1,2,1) # 1 fila, 2 columnas primer subplot
sns.boxplot(y=df["duration"])
plt.title("Box plots - Con Outliers")
plt.xlabel("Duracion")
plt.ylabel("Minutos")

Q3 = df["duration"].quantile(0.75)
Q1 = df["duration"].quantile(0.25)
# quant_df  = df.quantile([0.25, 0.75])

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
#plt.show()
