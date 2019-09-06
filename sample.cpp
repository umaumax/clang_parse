#include <iostream>
#include <string>

struct GoodStructName {
  float good_struct_field_name;
};

struct bad_struct_name {
  float badStructFieldName;
  float bad_struct_field_name_;
};

class GoodClassName {
 private:
  void GoodMethodName(){};
  float good_class_field_name_;
};

template <class T>
class GoodClassTemplateName {
 private:
  void GoodMethodName(){};
  T good_class_field_name_;
};

class bad_class_name {
 private:
  void bad_method_name(){};
  float bad_class_field_name;
};

void GoodFuncName(int good_arg_name) {}
void bad_func_name(int badArgName) {}

int main(int argc, char* argv[]) {
  int good_var_name  = 0;
  int good_var_name1 = 1, good_var_name2 = 2;

  int badVarName  = 0;
  int badVarName1 = 1, badVarName2 = 2;
  return 0;
}
