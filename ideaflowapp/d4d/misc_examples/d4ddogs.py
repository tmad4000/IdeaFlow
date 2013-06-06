import os, sys
sys.path.append(os.path.abspath("../"))
from d4d import d4d

d4d.normalize("d1", 
              """cats desire food
                 dogs desire food
                 cats desire fish
              """,
              principal_component_count=1)

d4d.d1.how_true_is("dogs desire fish")

d4d.normalize("d1", 
              """cats desire food
                 dogs desire food
                 cats desire outdoors
                 dogs desire outdoors
                 cats desire human
                 dogs desire human
                 cats desire warmth
                 dogs desire warmth
                 cats desire fish              
              """,
    principal_component_count=3)

d4d.d1.how_true_is("dogs desires fish")