from database.DB_connect import DBConnect


class DAO():
    @staticmethod
    def getNodes():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """ select distinct g.Chromosome  from genes g where g.Chromosome != 0 """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row[0])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getNodesDueZ():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """ select distinct c.Localization  from classification c  """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append(row[0])
        cursor.close()
        cnx.close()
        return result


    @staticmethod
    def getEdges():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """select distinct c_1, c_2, sum(expr)
                from (
                select distinct g1.Chromosome as c_1, g2.Chromosome as c_2, 
                g1.GeneID as g_id1, g2.GeneID as g_id2, i.Expression_Corr as expr
                from interactions i, genes g1, genes g2
                where g1.GeneID = i.GeneID1 and g2.GeneID  = i.GeneID2
                    and g1.Chromosome <> g2.Chromosome
                    and g1.Chromosome <> 0
                    and g2.Chromosome <> 0
                order by g1.Chromosome ) as t
                group by c_1, c_2"""
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append([row[0], row[1], row[2]])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getEdgesDueZ():
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """select distinct c1.Localization, c2.Localization, count(distinct i.`Type`)  from classification c1 
                    left join classification c2 on c2.Localization != c1.Localization, interactions i
                    where c1.Localization < c2.Localization and ((c1.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2) or
                    (c1.GeneID = i.GeneID2 and c2.GeneID = i.GeneID1))
                    group by c1.Localization, c2.Localization """
        cursor.execute(query)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append([row[0], row[1], row[2]])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def getWeightTo(node1, node2):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """select sum(i.Expression_Corr) from interactions i, (select distinct g1.GeneID as g1, g2.GeneID as g2 from genes g1,
                    genes g2 where g1.Chromosome = %s and g2.Chromosome = %s and g1.GeneID != g2.GeneID) as sub
                    where sub.g1 = i.GeneID1 and sub.g2 = i.GeneID2  """
        cursor.execute(query, (node1, node2))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row[0]

    @staticmethod
    def getWeightFrom(node1, node2):
        cnx = DBConnect.get_connection()

        cursor = cnx.cursor()
        query = """select sum(i.Expression_Corr) from interactions i, (select distinct g1.GeneID as g1, g2.GeneID as g2 from genes g1,
                        genes g2 where g1.Chromosome = %s and g2.Chromosome = %s and g1.GeneID != g2.GeneID) as sub
                        where sub.g1 = i.GeneID1 and sub.g2 = i.GeneID2  """
        cursor.execute(query, (node2, node1))
        row = cursor.fetchone()
        cursor.close()
        cnx.close()
        return row[0]



