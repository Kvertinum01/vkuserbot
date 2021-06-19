class VkuserbotClass:
    def __repr__(self) -> str:
        res_class_info = self.__class__.__name__ + "("
        class_vars = []
        for name, value in self.__dict__.items():
            if name[0] == "_":
                continue
            class_vars.append(name + "=" + str(value))
        str_class_vars = ", ".join(class_vars)
        res_class_info += str_class_vars + ")"
        return res_class_info