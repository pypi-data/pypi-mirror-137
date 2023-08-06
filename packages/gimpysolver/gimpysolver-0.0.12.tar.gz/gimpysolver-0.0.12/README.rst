Readme!
=======

This is a simple and specific solver to gimpy captcha types like SEACE
PORTAL. The model has been trained with 4000 images and 92 porcent of
accuracy.

steps
=====

1. pip install gimpysolver
2. Import the package like: from gimpysolver import captchaSolverRPA
3. Create your first object captchasolver. myCaptcha =
   captchaSolverRPA.captcha_solver(path_img). *Where path_img es where
   you image exist.* **Caution** Only read \*.png images and size image
   would be 380,85
4. If you don’t meet requirements about image dimension you can resize
   with: myCaptcha.resize()
5. To solve captcha you can call predict method: myCaptcha.predict()

**Gimpy captcha SEACE
example**\ \*!:https://i.ibb.co/RNHtgm5/captcha-capture-1.png
