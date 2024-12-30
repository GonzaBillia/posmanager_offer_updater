cod1 = 'SET @codigoInterno1 = 1;'
cod2 = 'SET @codigoInterno2 = 8001;'

Q_PRODUCTS = """
    SELECT 
        CASE
            WHEN productos.idItem IN (5, 7) AND LENGTH(LTRIM(productos.Codebar)) <= 5 THEN 
                CAST(LTRIM(productos.Codebar) AS UNSIGNED)
            WHEN productos.idItem IN (5, 7) AND LENGTH(LTRIM(productos.Codebar)) > 5 THEN 
                (@codigoInterno1 := @codigoInterno1 + 1)
            ELSE 
                (@codigoInterno2 := @codigoInterno2 + 1)
        END AS codigoInterno,

        CONCAT ( productos.Producto,' ', productos.Presentacion) AS 'Nom Reducido',
        productos.idItem,
        productos.idTipoIVA,
        IFNULL(subrubros.idCategoria, 0) AS idCategoria,
        IFNULL(productos.IDSubRubro, 0) AS IDSubRubro,
        0 AS 'Codigo_de_Envase_asociado',
        0 AS 'Porc_de_Impuesto_Interno',

        ROUND(
            CASE 
                WHEN productos.idItem = 5 THEN 
                    ROUND(
                        (productos.Costo + 
                            CASE 
                                WHEN productos.idTipoIVA = 1 THEN 0
                                WHEN productos.idTipoIVA = 2 THEN productos.Costo * 0.105
                                WHEN productos.idTipoIVA = 3 THEN productos.Costo * 0.21
                                WHEN productos.idTipoIVA = 4 THEN productos.Costo * 0.27
                                ELSE 0
                            END
                        ) * (1 + productos.MargenPVP / 100),
                        2
                    ) * 1000
                ELSE 
                    ROUND(
                        (productos.Costo + 
                            CASE 
                                WHEN productos.idTipoIVA = 1 THEN 0
                                WHEN productos.idTipoIVA = 2 THEN productos.Costo * 0.105
                                WHEN productos.idTipoIVA = 3 THEN productos.Costo * 0.21
                                WHEN productos.idTipoIVA = 4 THEN productos.Costo * 0.27
                                ELSE 0
                            END
                        ) * (1 + productos.MargenPVP / 100),
                        2
                    )
            END,
            2 
        ) AS precio_final,

        productos.FechaUltimoPrecio,
        CONCAT ( productos.Producto,' ', productos.Presentacion) AS 'descrip reducida',
        'N' AS 'Eliminacion_de_item',
        '1' AS 'Tipo de Unidad',
        '1' AS 'Unidad',
        '5' AS 'Dias_de_Vencimiento',
        '0' AS 'Tamanio de Letra',
        productos.FechaUltimoPrecio,
        '*' AS 'Codigo_Adicional',
        'N' AS 'Permite_Modif_Descripcion',
        '0' AS 'Precio adicional de venta con IVA',
        '-1' AS 'Codigo de Plantilla de Etiqueta',
        '0' AS 'Codigo de IVA Diferencial',
        productos.UltimoPrecio,
        ' ' AS 'Precio_de_Oferta_Etiquetas',
        productos.IDProducto,
        ' ' AS 'Codigo_de_envase_asociado_ERP',
        '-1' AS 'Monto_de_Impuesto_Interno',
        productos.idTipoIVA,
        'N' AS 'Aplica_Percepcion_5329',
        '-1' AS 'Costo _el_articulo',
        IFNULL(productos.idProveedor, 0) AS idProveedor,
        IFNULL(productos.IDRubro, 0) AS IDRubro,
        IFNULL(productos.idMarca, 0) AS idMarca,  -- IFNULL en idMarca
        '01/12/2024' AS 'Fecha Inicio',
        '31/12/2024' AS 'Fecha Fin'

    FROM 
        productos
        LEFT JOIN Subrubros
        ON productos.IDSubRubro = subrubros.IDSubRubro

    WHERE productos.Activo = 's'
    AND productos.FechaModificacion >= CURDATE() - %(day_filter)s
    AND productos.idTipoIVA != 1
    GROUP BY codigoInterno;
"""

Q_UPDATED_PRODUCTS = """
    SELECT 
        CASE
            WHEN productos.idItem IN (5, 7) AND LENGTH(LTRIM(productos.Codebar)) <= 5 THEN 
                CAST(LTRIM(productos.Codebar) AS UNSIGNED)
            WHEN productos.idItem IN (5, 7) AND LENGTH(LTRIM(productos.Codebar)) > 5 THEN 
                (@codigoInterno1 := @codigoInterno1 + 1)
            ELSE 
                (@codigoInterno2 := @codigoInterno2 + 1)
        END AS codigoInterno,

        CONCAT ( productos.Producto,' ', productos.Presentacion) AS 'Nom Reducido',
        productos.idItem,
        productos.idTipoIVA,
        IFNULL(subrubros.idCategoria, 0) AS idCategoria,
        IFNULL(productos.IDSubRubro, 0) AS IDSubRubro,
        0 AS 'Codigo_de_Envase_asociado',
        0 AS 'Porc_de_Impuesto_Interno',

        ROUND(
            CASE 
                WHEN productos.idItem = 5 THEN 
                    ROUND(
                        (productos.Costo + 
                            CASE 
                                WHEN productos.idTipoIVA = 1 THEN 0
                                WHEN productos.idTipoIVA = 2 THEN productos.Costo * 0.105
                                WHEN productos.idTipoIVA = 3 THEN productos.Costo * 0.21
                                WHEN productos.idTipoIVA = 4 THEN productos.Costo * 0.27
                                ELSE 0
                            END
                        ) * (1 + productos.MargenPVP / 100),
                        2
                    ) * 1000
                ELSE 
                    ROUND(
                        (productos.Costo + 
                            CASE 
                                WHEN productos.idTipoIVA = 1 THEN 0
                                WHEN productos.idTipoIVA = 2 THEN productos.Costo * 0.105
                                WHEN productos.idTipoIVA = 3 THEN productos.Costo * 0.21
                                WHEN productos.idTipoIVA = 4 THEN productos.Costo * 0.27
                                ELSE 0
                            END
                        ) * (1 + productos.MargenPVP / 100),
                        2
                    )
            END,
            2 
        ) AS precio_final,

        productos.FechaUltimoPrecio,
        CONCAT ( productos.Producto,' ', productos.Presentacion) AS 'descrip reducida',
        'N' AS 'Eliminacion_de_item',
        '1' AS 'Tipo de Unidad',
        '1' AS 'Unidad',
        '5' AS 'Dias_de_Vencimiento',
        '0' AS 'Tamanio de Letra',
        productos.FechaUltimoPrecio,
        '*' AS 'Codigo_Adicional',
        'N' AS 'Permite_Modif_Descripcion',
        '0' AS 'Precio adicional de venta con IVA',
        '-1' AS 'Codigo de Plantilla de Etiqueta',
        '0' AS 'Codigo de IVA Diferencial',
        productos.UltimoPrecio,
        ' ' AS 'Precio_de_Oferta_Etiquetas',
        productos.IDProducto,
        ' ' AS 'Codigo_de_envase_asociado_ERP',
        '-1' AS 'Monto_de_Impuesto_Interno',
        productos.idTipoIVA,
        'N' AS 'Aplica_Percepcion_5329',
        '-1' AS 'Costo _el_articulo',
        IFNULL(productos.idProveedor, 0) AS idProveedor,
        IFNULL(productos.IDRubro, 0) AS IDRubro,
        IFNULL(productos.idMarca, 0) AS idMarca,  -- IFNULL en idMarca
        '01/12/2024' AS 'Fecha Inicio',
        '31/12/2024' AS 'Fecha Fin'

    FROM 
        productos
        LEFT JOIN Subrubros
        ON productos.IDSubRubro = subrubros.IDSubRubro

    WHERE 
        productos.Activo = 's'
        AND productos.idTipoIVA != 1
    GROUP BY 
        codigoInterno;
"""

Q_BARCODES = """
    SELECT productoscodebars.IDProducto AS IDProducto, 
           IFNULL(productoscodebars.codebar, '0') AS Codebar  -- IFNULL en Codebar
    FROM productoscodebars 
    LEFT JOIN productos
    ON productos.IDProducto = productoscodebars.IDProducto
    WHERE productos.Activo = 's' 
    UNION ALL

    SELECT productos.IDProducto AS IDProducto, 
           IFNULL(productos.Codebar, '0') AS Codebar
    FROM productos
    WHERE productos.Activo = 's' 
"""

Q_DEPARTMENTS = """
    SELECT 
        IDCategoria,
        Nombre 
    FROM 
        categorias
"""

Q_FAMILIES = """
    SELECT 
        IDSubRubro,
        Nombre 
    FROM 
        subrubros
"""

Q_PROVIDERS = """
    SELECT
        IDProveedor,
        Nombre
    FROM
        proveedores
"""