TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "listar_usuarios",
            "description": "Lista todos los usuarios del sistema SENA.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_usuario",
            "description": "Busca usuario por nombre o email. "
                           "SIEMPRE usarlo antes de crear o asignar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {"type": "string", "description": "Nombre o email"}
                },
                "required": ["q"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_usuario",
            "description": "Crea un nuevo usuario. "
                           "Solo si buscar_usuario no lo encontró.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre":   {"type": "string"},
                    "email":    {"type": "string"},
                    "password": {"type": "string"},
                    "rol":      {"type": "string",
                                 "enum": ["admin","instructor","aprendiz"]}
                },
                "required": ["nombre","email","password","rol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_proyecto",
            "description": "Crea un nuevo proyecto en el sistema.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre":      {"type": "string"},
                    "descripcion": {"type": "string"},
                    "ficha":       {"type": "string"}
                },
                "required": ["nombre","descripcion","ficha"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "asignar_usuario_a_proyecto",
            "description": "Asigna un usuario a un proyecto. "
                           "Requiere IDs numéricos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "usuario_id":  {"type": "integer"},
                    "proyecto_id": {"type": "integer"}
                },
                "required": ["usuario_id","proyecto_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_proyectos",
            "description": "Devuelve todos los proyectos registrados en el sistema.",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]