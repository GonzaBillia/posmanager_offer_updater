P_STOCK = """
    SELECT 
        medicamentos.CodPlex AS 'IDProducto',
        stock.Cantidad
    FROM 
        medicamentos
    INNER JOIN 
        stock
    ON 
        medicamentos.CodPlex = stock.IDProducto
    WHERE 
        stock.Sucursal = 33
        AND stock.Cantidad != 0
"""