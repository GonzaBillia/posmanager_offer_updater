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

P_PRODUCTS = """
    SELECT
        -- (1)  codigoInterno
        '370000' AS codigoInterno,

        -- (2)  Nom Reducido
        m.Producto AS 'Nom Reducido',

        -- (3)  IdItem
        m.idTipoVenta AS idItem,

        -- (4)  idTipoIVA
        m.idTipoIVA AS idTipoIVA,

        -- (5)  idCategoria
        IFNULL(subrubros.idCategoria, 0) AS idCategoria,

        -- (6)  IDSubRubro
        IFNULL(m.IDSubRubro, 0) AS IDSubRubro,

        -- (7)  Codigo_de_Envase_asociado
        0 AS 'Codigo_de_Envase_asociado',

        -- (8)  Porc_de_Impuesto_Interno
        0 AS 'Porc_de_Impuesto_Interno',

        -- (9)  precio_final
        ROUND(COALESCE(mp.Precio, 0) / NULLIF(mp.Unidades, 0), 2) AS precio_final,

        -- (10) FechaUltimoPrecio
        DATE_FORMAT(m.FechaModificacion, '%d/%m/%Y') AS FechaUltimoPrecio,

        -- (11) descrip reducida
        m.Producto AS 'descrip reducida',

        -- (12) Eliminacion_de_item
        'N' AS 'Eliminacion_de_item',

        -- (13) Tipo de Unidad
        '1' AS 'Tipo de Unidad',

        -- (14) Unidad
        '1' AS 'Unidad',

        -- (15) Dias_de_Vencimiento
        '5' AS 'Dias_de_Vencimiento',

        -- (16) Tamanio de Letra
        '0' AS 'Tamanio de Letra',

        -- (17) FechaUltimoPrecio (segunda vez)
        DATE_FORMAT(m.FechaModificacion, '%d/%m/%Y') AS FechaUltimoPrecio,

        -- (18) Codigo_Adicional
        '*' AS 'Codigo_Adicional',

        -- (19) Permite_Modif_Descripcion
        'N' AS 'Permite_Modif_Descripcion',

        -- (20) Precio adicional de venta con IVA
        '0' AS 'Precio adicional de venta con IVA',

        -- (21) Codigo de Plantilla de Etiqueta
        '-1' AS 'Codigo de Plantilla de Etiqueta',

        -- (22) Codigo de IVA Diferencial
        '0' AS 'Codigo de IVA Diferencial',

        -- (23) UltimoPrecio
        IFNULL(m.Precio, 0) AS UltimoPrecio,

        -- (24) Precio_de_Oferta_Etiquetas
        ' ' AS 'Precio_de_Oferta_Etiquetas',

        -- (25) IDProducto
        m.CodPlex AS IDProducto,

        -- (26) Codigo_de_envase_asociado_ERP
        ' ' AS 'Codigo_de_envase_asociado_ERP',

        -- (27) Monto_de_Impuesto_Interno
        '-1' AS 'Monto_de_Impuesto_Interno',

        -- (28) idTipoIVA (segunda aparición)
        m.idTipoIVA AS idTipoIVA,

        -- (29) Aplica_Percepcion_5329
        'N' AS 'Aplica_Percepcion_5329',

        -- (30) Costo _el_articulo
        '-1' AS 'Costo _el_articulo',

        -- (31) idProveedor
        IFNULL(m.idProveedor, 0) AS idProveedor,

        -- (32) IDRubro
        IFNULL(m.CodRubro, 0) AS IDRubro,

        -- (33) idMarca
        IFNULL(m.CodLab, 0) AS idMarca,

        -- (34) Fecha Inicio
        '01/12/2024' AS 'Fecha Inicio',

        -- (35) Fecha Fin
        '31/12/2024' AS 'Fecha Fin'
    FROM onze_center.medicamentos AS m
    LEFT JOIN onze_center.medicamentos AS mp
        ON mp.CodPlex = m.IdProductoPadre
    INNER JOIN onze_center.stock AS s
        ON m.CodPlex = s.IDProducto
    LEFT JOIN Subrubros
        ON m.IDSubRubro = subrubros.IDSubRubro
    WHERE m.IdProductoPadre != ''
    AND m.visible = True
    AND s.Sucursal = '33'
    AND s.Cantidad != 0
    AND m.CodPlex LIKE '999%';
"""