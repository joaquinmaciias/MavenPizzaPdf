from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf.enums import XPos, YPos
import re

def Pdf(dict_pizza_orders: dict, dict_ingredients_weekly: dict):

    pdf = FPDF('P','mm','A4')

    pdf.set_auto_page_break(auto = True, margin = 10) # Ajustamos los margenes del pdf

    pdf.add_page() # Añadimos una pagina

    pdf.set_author('Joaquin Mir') # Autor del pdf

    # Cabezera hojas

    pdf.image('logo_icai.jpg', 10, 8, 40)

    pdf.set_font('Arial', 'BU', size = 25)
    pdf.cell(210,10, align = 'C', txt = 'Informe Maven Pizza', border = False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


    pdf.set_font('Arial', 'I', size = 15)
    pdf.cell(210,10, align = 'C', txt = 'Joaquin Mir Macias', border = False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


    # Primera gráfica

    pdf.set_font('Arial', 'U', size = 15)
    pdf.cell(90,30, align = 'C', txt = 'Cantidad de pizzas vendidas 2015: ', border = False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image('Pizzas_pedidas.jpg', 5, 55, 210)

    # Segunda gráfica

    pdf.set_font('Arial', 'U', size = 15)
    pdf.cell(90,209, align = 'C', txt = 'Cantidad de pizzas vendidas 2015: ', border = False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image('Ingredientes_semanales.jpg', 0, 167, 220)

    # Pie de hoja

    pdf.set_y(-20)
    pdf.set_font('Arial', 'I', 10)

    # pdf.page_no(), número de la página donde te encuentras
    # {nb}, número de páginas totales

    pdf.cell(0, 10, f'Page {pdf.page_no()}/{{nb}}', align = 'C')

    pdf.add_page() # Añadimos una pagina

    # Titulo
    pdf.set_font('Arial','BU',14)
    pdf.cell(120,25, align = 'C', txt = 'Pizzas vendidas',new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Columnas que aprecerán

    pdf.set_font('Arial','',14)
    pdf.cell(30,10, align = 'C', txt = 'Pizzas')
    pdf.cell(110,10, align = 'C', txt = 'Cantidad', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Recorremos el dataframe final con los ingredientes añadiendo
    # en la columna correspondiente el nombre del ingrediente y las raciones necesarias

    pdf.set_font('Arial','',10)
    for key in dict_pizza_orders:

        ingrediente = str(key)
        cantidad = str(dict_pizza_orders[key])
        pdf.cell(70,5,txt = ingrediente)
        pdf.cell(70,5,txt = cantidad,new_x=XPos.LMARGIN, new_y=YPos.NEXT)


    # Pie de hoja

    pdf.set_y(-20)
    pdf.set_font('Arial', 'I', 10)

    # pdf.page_no(), número de la página donde te encuentras
    # {nb}, número de páginas totales

    pdf.cell(0, 10, f'Page {pdf.page_no()}/{{nb}}', align = 'C')

    pdf.add_page() # Añadimos una pagina

    # Titulo
    pdf.set_font('Arial','BU',14)
    pdf.cell(120,25, align = 'C', txt = 'Cantidad de ingredientes por semana',new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Columnas que aprecerán

    pdf.set_font('Arial','',14)
    pdf.cell(30,10, align = 'C', txt = 'Ingredientes')
    pdf.cell(110,10, align = 'C', txt = 'Cantidad', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Recorremos el dataframe final con los ingredientes añadiendo
    # en la columna correspondiente el nombre del ingrediente y las raciones necesarias

    pdf.set_font('Arial','',10)
    for key in dict_ingredients_weekly:

        ingrediente = str(key)
        cantidad = str(dict_ingredients_weekly[key])
        pdf.cell(70,5,txt = ingrediente)
        pdf.cell(70,5,txt = cantidad,new_x=XPos.LMARGIN, new_y=YPos.NEXT)


        # Pie de hoja

    pdf.set_y(-20)
    pdf.set_font('Arial', 'I', 10)

    # pdf.page_no(), número de la página donde te encuentras
    # {nb}, número de páginas totales

    pdf.cell(0, 10, f'Page {pdf.page_no()}/{{nb}}', align = 'C')



    pdf.output('MavenPizza.pdf')



def extract(csv_file: str) -> pd.DataFrame:  # Extraemos los datos de los csv

    df = pd.read_csv(csv_file)

    return df


def transform_orders(df: pd.DataFrame):  # Transformamos los datos de los dataframes

    pizza_rep = dict()
    df_pizza_quantity = df.loc[:, ['pizza_id', 'quantity']]  # Nos guardamos las columnas que nos interesan del dataframe
    list_pizza_quantity = df_pizza_quantity.values.tolist()  # Pasamos el dataframe a una lista

    # Eliminamos con expresiones regulares el tamaño de la pizza que acompaña al nombre de la pizza

    for i in range(len(list_pizza_quantity)):
        list_pizza_quantity[i][0] = re.sub('_[a-z]$', '', list_pizza_quantity[i][0])

    # Creamos un diccionario con claves los nombres de las pizzas y sus valores el número de veces que fueron pedidas.

    for i in range(len(list_pizza_quantity)):
        try:
            pizza_rep[list_pizza_quantity[i][0]] += 1
        except:
            pizza_rep[list_pizza_quantity[i][0]] = 1

    return pizza_rep


def transform_ingredients(df: pd.DataFrame, dict_orders:dict) -> dict: 

    dict_ingredients = dict()
    df_pizza_ingredients = df.loc[:, ['pizza_type_id','ingredients']]
    list_pizza_ingredients = df_pizza_ingredients.values.tolist()

    for i in range(len(list_pizza_ingredients)):
        list_pizza_ingredients[i][1] = list_pizza_ingredients[i][1].replace(', ', ',')
        list_pizza_ingredients[i][1] = re.findall(r'([^,]+)(?:,|$)', list_pizza_ingredients[i][1])
        # list_pizza_ingredients[i] = [nombre pizza,[ingrediente(1),...,ingrediente(k)]]

    for typepizza in range(len(list_pizza_ingredients)):

        for ingredients in range(len(list_pizza_ingredients[typepizza][1])):

            number_order_pizza = dict_orders[list_pizza_ingredients[typepizza][0]]  # Numero de veces que se pedio la pizza con dicho ingrerdiente

            try:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza + dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]]
            except:
                dict_ingredients[list_pizza_ingredients[typepizza][1][ingredients]] = number_order_pizza

    return dict_ingredients

def load_graphic_pizzas(pizza_rep: dict) -> pd.DataFrame :

    df  = pd.DataFrame()

    list_type_pizza = []
    list_quantity = []

    for key in pizza_rep:
        list_type_pizza.append(key)
        list_quantity.append(pizza_rep[key])


    df['pizza_id'] = list_type_pizza
    df['quantity'] = list_quantity

    plt.rcParams.update({'font.size': 24})
    plt.figure(figsize=(50, 25))
    ax = sns.barplot(x='pizza_id', y='quantity', data=df,palette='rocket_r')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=70)
    ax.set_title('Pizzas pedidas')
    plt.savefig('Pizzas_pedidas.jpg')




def load_graphic_ingredients(dict_ingredients_weekly: dict,):

    # Dict -> DataFrame

    df = pd.DataFrame()
    ingredients = []
    quantity = []

    for key in dict_ingredients_weekly:
        quantity.append(key)
        ingredients.append(dict_ingredients_weekly[key])

    df['Cantidad'] = quantity
    df['Ingredientes'] = ingredients

    plt.rcParams.update({'font.size': 24})
    plt.figure(figsize=(50, 25))
    ax = sns.barplot(x='Cantidad', y='Ingredientes', data=df,palette='rocket_r')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=70)
    ax.set_title('Ingredientes semanales')
    plt.savefig('Ingredientes_semanales.jpg')



if __name__ == '__main__':


    # Seguiremos el preceso ETL

    # Extract
    order_details = extract('order_details.csv')
    pizzas = extract('pizzas.csv')
    pizza_types = extract('pizza_types.csv')

    # Analisis
    # details_csv('order_details.csv',order_details)
    # details_csv('pizzas.csv',pizzas)
    # details_csv('pizza_types.csv',pizza_types)

    # Transform
    dict_pizza_orders = transform_orders(order_details)
    dict_ingredients_anual  = transform_ingredients(pizza_types, dict_pizza_orders)
    load_graphic_pizzas(dict_pizza_orders)

    # Ingredients semanales

    dict_ingredients_weekly = dict()

    for key in dict_ingredients_anual:

        dict_ingredients_weekly[key] = dict_ingredients_anual[key] / 12 * 4

    # print('Para stock de ingredientes deberian comprar a la semana -->\n')
    # print('El consumo de cada ingredientes medio por semana es de: ')

    # for key in dict_ingredients_weekly:
    #     print(f'{key}: {int(dict_ingredients_weekly[key])}')

    load_graphic_ingredients(dict_ingredients_weekly)

    Pdf(dict_pizza_orders, dict_ingredients_weekly)