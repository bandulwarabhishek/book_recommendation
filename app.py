from flask import Flask, jsonify, request, render_template
import pickle
import re
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors



top_50 = pickle.load(open("model/top_50.pkl","rb"))
books = pickle.load(open("model/books.pkl","rb"))
similarity = pickle.load(open("model/similarity_scores.pkl","rb"))
pivot_table = pickle.load(open("model/pivot_table.pkl","rb"))

app = Flask(__name__)

# Define the route to be home
# The decorator below links the relative route of the URL to the function it is decorating 
# Here, home function is with '/ ',our root directory
# Running the app sends us to index,html
# Note that render_template means it looks for the file in the templates folder

# -------------------------------------------------------------------------------------------------------------

def get_country_books():

    if 'books' not in globals():
        raise   ValueError("Error: The 'books' dataframe is not defined.")
    
    # Filter the books DataFrame for Indian books
    sorted_books = books[books['Country']=='india']
    sorted_books = sorted_books.drop_duplicates('Book_Title_title')
    sorted_books = sorted_books.sort_values(by='popularity_score',ascending=False).head(20)[['Book_Title_title','Image-URL-S','Book_Author_title','Publisher_title']]
    
    country = sorted_books.to_dict(orient='list')

    return country

# ------------------------------------------------------------------------------------------------------------

def get_top50_books():
    
    return {  
        "book_name": list(top_50['Book_Title_title'].values),
        "book_ratings": list(top_50['No_of_ratings'].values),
        "book_image": list(top_50['Image-URL-S'].values),
        "book_author": list(top_50['Book_Author_title'].values),
        "book_publisher": list(top_50['Publisher_title'].values)    
        }

# -----------------------------------------------------------------------------------------------------------

def get_books_childs():
    books_for_child = books[(books['age_group']== 'Child') & (books['No_of_ratings'] > 500)].sort_values(by='No_of_ratings',ascending=False).drop_duplicates('Book_Title_title')

    books_for_child= books_for_child[['Book_Title_title','Image-URL-S','Book_Author_title','Publisher_title']]

    #Convert the DataFrame to a list of dictionaries
    item = books_for_child.to_dict(orient='list')
    
    return item
# ---------------------------------------------------------------------------------------------------------

def get_books_adults():
    books_for_adults =books[(books['age_group']== 'Adult') & (books['No_of_ratings'] > 500)].sort_values(by='No_of_ratings',ascending=False).drop_duplicates('Book_Title_title')

    books_for_adults= books_for_adults[['Book_Title_title','Image-URL-S','Book_Author_title','Publisher_title']]

    #Convert the DataFrame to a list of dictionaries
    item = books_for_adults.to_dict(orient='list')

    return item
# ----------------------------------------------------------------------------------------------------------

def get_books_senior():
    books_for_senior = books[(books['age_group']== 'Senior') & (books['No_of_ratings'] > 500)].sort_values(by='No_of_ratings',ascending=False).drop_duplicates('Book_Title_title')

    books_for_senior= books_for_senior[['Book_Title_title','Image-URL-S','Book_Author_title','Publisher_title']]

    #Convert the DataFrame to a list of dictionaries
    item = books_for_senior.to_dict(orient='list')
    
    return item

# ----------------------------------------------------------------------------------------------------------

# The function below is the main function that runs the Flask app
@app.route('/')
def index():
    top_50_data = get_top50_books()
    books_for_child = get_books_childs()
    books_for_adult = get_books_adults()
    books_for_senior = get_books_senior()
    country_books = get_country_books()

    # print(books_for_child)    
    # print("\n\n\ntop 50 books:", top_50_data)  # Debugging step
    return render_template("index.html",top_50=top_50_data, data=books_for_child, adult_books=books_for_adult, elderly_book=books_for_senior, countrywise_data=country_books)  # Pass data to template


# @app.route('/home')
# def home():
#     books_for_child = get_books_childs()
#     print(books_for_child)
#     return render_template("home.html",data=books_for_child)


@app.route('/recommend_books',methods=['POST'])
def recommend_books():

    
    if request.method=="GET":
        return render_template('index.html')
    else:
        user_input = request.form.get('user_input')
        #converting to lowercase and removing all the special characters
        processed = re.sub("[^a-zA-Z0-9 ]","",user_input.lower())
        
        try:
            #index fetch
            index = np.where(pivot_table.index == processed)[0][0]
            #fetching similar books
            similar_books = sorted(list(enumerate(similarity[index])), key=lambda x:x[1],reverse=True)[1:10]

            data = []
            for i in similar_books:
                item = []
    #             print(pt_df.index[i[0]])#i[0]-will return the index value of the similar movies, passing it into dataframe prints its corresponding movie name
                temp_df = books[books['Book_Title_title'] == pivot_table.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book_Title_title')['Book_Title_title'].values))#drop all the duplicates record because same books were having different ISBN hence drop on Book-tile cloumn
                item.extend(list(temp_df.drop_duplicates('Book_Title_title')['Book_Author_title'].values))
                item.extend(list(temp_df.drop_duplicates('Book_Title_title')['Image-URL-S'].values))
                item.extend(list(temp_df.drop_duplicates('Book_Title_title')['Publisher_title'].values))
                
                data.append(item)
                
        except Exception as e:
            print(f"Books similar to {user_input} not found")
    #         print(f"An exception occurred: {e}")

    return render_template('recommend.html',data=data)



if __name__ == '__main__':
    app.run(debug=True)
