from flask import Flask, request, render_template
import pickle
import re
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity = pickle.load(open('similarity_scores.pkl','rb'))
user_movie = pickle.load(open('user_movie.pkl','rb'))

app = Flask(__name__)

# Define the route to be home
# The decorator below links the relative route of the URL to the function it is decorating 
# Here, home function is with '/ ',our root directory
# Running the app sends us to index,html
# Note that render_template means it looks for the file in the templates folder

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(popular_df['Book_Title_title'].values),
                           book_ratings = list(popular_df['No_of_ratings'].values),
                           book_image = list(popular_df['Image-URL-S'].values),
                           book_author = list(popular_df['Book_Author_title'].values),
                           book_publisher = list(popular_df['Publisher_title'].values)
                           )


@app.route('/recommend')
def recommend_page():
    return render_template("recommend.html")


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
            index = np.where(user_movie.index == processed)[0][0]
            #fetching similar books
            similar_books = sorted(list(enumerate(similarity[index])), key=lambda x:x[1],reverse=True)[1:10]

            data = []
            for i in similar_books:
                item = []
    #             print(pt_df.index[i[0]])#i[0]-will return the index value of the similar movies, passing it into dataframe prints its corresponding movie name
                temp_df = books[books['Book_Title_title'] == user_movie.index[i[0]]]
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
