import pymysql


def query_member_by_ada(ada_list):
    """
    根据 ADA 列表查询会员信息
    :param ada_list: ADA 值列表，如 ['9922333']
    :return: 查询结果列表，每个元素是一个字典
    """
    config = {
        'host': 'uat-ecom-uc-common-auroramysql-proxy.proxy-cnqrvhokxvig.ap-northeast-1.rds.amazonaws.com',
        'user': 'ne_uc_app_uat',
        'password': 'bRgFlp$j8YNYdBZ84UWSLNtrd6cBVl',
        'database': 'tw_ne_uc_uat',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }

    results = []

    try:
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            # 构建安全的 SQL 查询
            placeholders = ','.join(['%s'] * len(ada_list))
            sql = f"SELECT * FROM um_member WHERE ADA IN ({placeholders})"
            cursor.execute(sql, ada_list)
            results = cursor.fetchall()

    except pymysql.Error as e:
        print(f"数据库错误: {e}")
    finally:
        if connection:
            connection.close()

    return results


def print_member_results(results):
    """格式化打印会员信息"""
    for row in results:
        print(f"ID: {row['id']}, 过期日期: {row['expire_date']}, 卡号: {row['ada']}")


# 如果是直接运行脚本，执行查询并打印结果
if __name__ == "__main__":
    ada_list = ['9922333']
    results = query_member_by_ada(ada_list)
    print_member_results(results)
