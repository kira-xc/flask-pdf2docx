from flask import Flask,send_file,render_template,request,redirect,url_for
import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename
from cript import sha256sum
app=Flask(__name__)
num=0

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
    
@app.route("/download")
def download():
    try:
        n=secure_filename(request.args["n"])
        return send_file("downloads/"+n,as_attachment=True)
    except:
        return render_template("error.html")
        
        
@app.route("/upload",methods=["POST","GET"])
def upload():
    global num
    num=0
    if request.method=="POST":
        if "filepdf" not in request.files:
            return render_template("error.html") 
        file=request.files.get("filepdf")
        if file.filename=="":
            return render_template("error.html")
        filepdf=str(num)+".pdf"
        while os.path.exists(os.path.join("uploads",filepdf)):
            num+=1
            filepdf=str(num)+".pdf"
        file.save(os.path.join("uploads",filepdf))
        return redirect(url_for("downloads",name=filepdf))
    if request.method=="GET":
        return render_template("index.html")

@app.route("/downloads")
def downloads():
    try:
        name=secure_filename(request.args["name"])
        pdf_file = 'uploads/'+name
        namedocx=sha256sum(pdf_file)+".docx"
        docx_file = 'downloads/'+namedocx
        
        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)      # all pages by default
        cv.close()
        os.remove(pdf_file)
        return render_template("download.html",nc=namedocx)
    except:
        return render_template("error.html")


    
    



