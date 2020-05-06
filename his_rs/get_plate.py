# -*- coding: UTF-8 -*-

# 导入 futu-api
import futu as ft
import time
import os
import shutil
import pandas as pd


def get_all_market_plate_stock_rs():
    # 获取时间戳
    time_now = time.strftime("%Y%m%d", time.localtime(time.time()))
    # print(time_now)
    path = "./data/" + time_now + "/"
    # 如果路径存在着删除
    if os.path.exists(path) is True:
        try:
            print("删除已存在路径")
            shutil.rmtree(path)
        except IOError as err:
            print("路径删除异常")
    os.mkdir(path)
    # 实例化行情上下文对象
    quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)
    # quote_ctx = ft.OpenQuoteContext(host="118.25.176.152", port=11111)
    # 按市场获取四分位

    # 按板块获取四分位
    get_plate_stock_rs("HK", path, quote_ctx)
    # get_plate_stock_rs("SZ", path)
    # get_plate_stock_rs("SH", path)
    quote_ctx.close()


def get_plate_stock_rs(market, path, quote_ctx):
    # 实例化行情上下文对象
    # quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

    # 上下文控制
    # quote_ctx.start()              # 开启异步数据接收
    # quote_ctx.set_handler(ft.TickerHandlerBase())  # 设置用于异步处理数据的回调对象(可派生支持自定义)

    # print(quote_ctx.get_plate_stock('HK.Motherboard'))
    # print(quote_ctx.get_plate_list("HK", "ALL"))
    # 板块
    plate = quote_ctx.get_plate_list(market, "ALL")[1]
    # 保存板块信息
    plate_file_name = path + market + ".plate.csv"
    plate.to_csv(plate_file_name, encoding='utf-8-sig')

    # 板块代码列表
    plate_code_list = plate["code"].tolist()
    # 加上所有港股市场板块代码 HK.BK1910
    plate_code_list.append("HK.BK1910")
    # 去掉港股通（深圳）HK.BK1922
    # plate_code_list.remove("HK.BK1922")

    # for test
    # 港股通（深圳）板块
    # plate_code_list = ["HK.BK1922"]
    # 电商及互联网
    # plate_code_list = ["HK.BK1058"]
    # plate_code_list = ["HK.BK1005"]
    # plate_code_list = ["HK.BK1000"]
    # plate_code_list = ["HK.BK1028"]

    print(plate_code_list)
    print(len(plate_code_list))
    # for test

    for plate_code in plate_code_list:
        # 板块代码
        print(plate_code)
        # 获取板块的股票代码
        # 获取板块下的股票
        # 请求协议ID: 3205
        # 30秒内请求最多10次
        plate_stock = quote_ctx.get_plate_stock(plate_code)[1]
        time.sleep(4)
        # print(plate_stock)
        # 保存各个板块的股票代码
        if plate_code == "HK.BK1910":
            plate_stock_file_name = path + "HK.Market" + ".csv"
        else:
            plate_stock_file_name = path + plate_code + ".csv"
        plate_stock.to_csv(plate_stock_file_name, encoding='utf-8-sig')
        # 板块的股票代码列表
        stock_code_list = plate_stock["code"].tolist()
        # 板块下所有股票快照
        # 请求协议ID: 3203
        # 每次可请求股票数最多400
        # 30秒内快照最多请求次数60
        # 大于400多次请求
        if len(stock_code_list) == 0:
            continue
        if len(stock_code_list) <= 400:
            market_snapshot = quote_ctx.get_market_snapshot(stock_code_list)[1][
                ["code", "last_price", "total_market_val", "open_price", "prev_close_price"]]
        else:
            # 前400
            market_snapshot = quote_ctx.get_market_snapshot(stock_code_list[:400])[1][
                ["code", "last_price", "total_market_val", "open_price", "prev_close_price"]]
            # 400往后
            requset_times = int(len(stock_code_list) / 400)
            for times in range(requset_times):
                market_snapshot = market_snapshot.append(quote_ctx.get_market_snapshot(
                    stock_code_list[int((times + 1) * 400):int((times + 2)) * 400])[1][
                                                             ["code", "last_price", "total_market_val", "open_price",
                                                              "prev_close_price"]])
        # test 筛选市值前
        # print("筛选市值前")
        # print(market_snapshot)
        # 只统计板块内总市值大于等于50亿港币的股票
        market_snapshot = market_snapshot[market_snapshot["total_market_val"] >= 5.0e9]
        # test 筛选市值后
        # print("筛选市值后")
        # print(market_snapshot)
        # 板块指数最新价
        # s = quote_ctx.get_market_snapshot(plate_code)
        # 若板块代码是 HK.BK1910 表示所有港股
        if plate_code == "HK.BK1910":
            # 板块指数最新价=恒生指数最新价
            plate_index_last_price = quote_ctx.get_market_snapshot("HK.800000")[1]["last_price"].tolist()[0]
            # 板块指数今日开盘价=恒生指数今日开盘价
            plate_index_open_price = quote_ctx.get_market_snapshot("HK.800000")[1]["open_price"].tolist()[0]
            # 板块指数昨收盘价=恒生指数昨收盘
            plate_index_prev_close_price = quote_ctx.get_market_snapshot("HK.800000")[1]["prev_close_price"].tolist()[0]
        else:
            # 板块指数最新价
            plate_index_last_price = quote_ctx.get_market_snapshot(plate_code)[1]["last_price"].tolist()[0]
            # 板块指数今日开盘价
            plate_index_open_price = quote_ctx.get_market_snapshot(plate_code)[1]["open_price"].tolist()[0]
            # 板块指数昨收盘价
            plate_index_prev_close_price = quote_ctx.get_market_snapshot(plate_code)[1]["prev_close_price"].tolist()[0]
        print("板块指数最新价 %f" % plate_index_last_price)
        print("板块指数今日开盘价 %f" % plate_index_open_price)
        print("板块指数昨收盘价 %f" % plate_index_prev_close_price)
        # 板块指数涨跌幅算法1 最新价/今日开盘价-1
        # plate_index_change_rate1 = plate_index_last_price / plate_index_open_price - 1
        # print("板块指数涨跌幅算法1 %f" % plate_index_change_rate1)
        # 板块指数涨跌幅算法2 最新价/昨收盘价-1
        plate_index_change_rate2 = plate_index_last_price / plate_index_prev_close_price - 1
        print("板块指数涨跌幅算法2 %f" % plate_index_change_rate2)
        # # 板块指数盘前涨跌幅
        # plate_index_pre_change_rate = quote_ctx.get_market_snapshot(plate_code)[1]["pre_change_rate"].tolist()[0]
        # if isinstance(plate_index_pre_change_rate, float):
        #     print("板块指数盘前涨跌幅 %f" % plate_index_pre_change_rate)
        # else:
        #     print("板块指数盘前涨跌幅 %s" % plate_index_pre_change_rate)
        # # 板块指数盘后涨跌幅
        # plate_index_after_change_rate = quote_ctx.get_market_snapshot(plate_code)[1]["after_change_rate"].tolist()[0]
        # if isinstance(plate_index_after_change_rate, float):
        #     print("板块指数盘后涨跌幅 %f" % plate_index_after_change_rate)
        # else:
        #     print("板块指数盘后涨跌幅 %s" % plate_index_after_change_rate)
        # 计算指标
        try:
            # 股票收盘价/板块指数收盘价
            market_snapshot["price_index_rate"] = market_snapshot['last_price'].apply(
                lambda x: x / plate_index_last_price)
            # 今开盘算涨跌幅1
            # market_snapshot["change_rate1"] = market_snapshot['last_price'] / market_snapshot['open_price'] - 1
            # 昨收盘计算涨跌幅2
            market_snapshot["change_rate2"] = market_snapshot['last_price'] / market_snapshot['prev_close_price'] - 1
            # 相对强弱rs1 股票涨跌幅1/板块指数涨幅幅1
            # market_snapshot["rs1"] = market_snapshot['change_rate1'].apply(
            #     lambda x: x / plate_index_change_rate1)
            # 相对强弱rs2 股票涨跌幅2/板块指数涨幅幅2
            market_snapshot["rs2"] = market_snapshot['change_rate2'].apply(
                lambda x: x / plate_index_change_rate2)
        except ZeroDivisionError as e:
            print("except:", e)
        # test 输出计算后完整结果
        # print(market_snapshot)
        # 排序-切片 四分位
        # result_len = int(len(market_snapshot) / 4)
        # if result_len < 1:
        #     print("板块数量不足，无法计算四分位")
        #     continue

        # 板块股票总数
        # 指数涨跌幅：涨
        # 股票涨跌幅 / 指数涨跌幅
        # 正相关排在前面，负相关在后，rs指标降序排
        # 指数涨跌幅：跌
        # 股票涨跌幅 / 指数涨跌幅
        # 负相关排在前面，正相关在后，rs指标升序排序
        # 市值按照降序排序
        if plate_index_change_rate2 > 0:
            sort_result = market_snapshot.sort_values(by=["rs2", "total_market_val"],
                                                      ascending=(False, False))
        else:
            sort_result = market_snapshot.sort_values(by=["rs2", "total_market_val"],
                                                      ascending=(True, False))
        total_len = len(sort_result)
        print("板块总长度，长度%d" % total_len)
        if total_len < 4:
            print("板块数量不足，无法计算四分位")
            # 直接输出结果
            if plate_code == "HK.BK1910":
                result_file_name = path + "HK.Market.result" + ".csv"
            else:
                result_file_name = path + plate_code + ".result" + ".csv"
            sort_result.to_csv(result_file_name, encoding='utf-8-sig')
            continue
        quart_len = int(total_len / 4)
        print("板块四分位长度，长度%d" % quart_len)
        # 第一四分位
        sort_result_first = sort_result.iloc[:quart_len]
        sort_result_first.insert(len(sort_result_first.columns), "quartile", 1)
        print("第一四分位，长度%d" % len(sort_result_first))
        print(sort_result_first)
        # 第二四分位
        sort_result_second = sort_result.iloc[quart_len:int(2 * quart_len)]
        sort_result_second.insert(len(sort_result_second.columns), "quartile", 2)
        print("第二四分位，长度%d" % len(sort_result_second))
        print(sort_result_second)
        # 第三四分位
        sort_result_third = sort_result.iloc[int(2 * quart_len):int(3 * quart_len)]
        sort_result_third.insert(len(sort_result_third.columns), "quartile", 3)
        print("第三四分位，长度%d" % len(sort_result_third))
        print(sort_result_third)
        # 第四四分位
        sort_result_fourth = sort_result.iloc[int(3 * quart_len):]
        sort_result_fourth.insert(len(sort_result_fourth.columns), "quartile", 4)
        print("第四四分位，长度%d" % len(sort_result_fourth))
        print(sort_result_fourth)
        # 四分位合并，用字段标识属于哪个分位
        rs2_result = pd.concat([sort_result_first, sort_result_second, sort_result_third, sort_result_fourth])
        # 增加四分位指标
        print(rs2_result)
        if plate_code == "HK.BK1910":
            result_file_name = path + "HK.Market.result" + ".csv"
        else:
            result_file_name = path + plate_code + ".result" + ".csv"
        rs2_result.to_csv(result_file_name, encoding='utf-8-sig')

    # 代码
    # code = plate_stock["code"].tolist()
    # print(type(code))
    # print(code)

    # market_snapshot = quote_ctx.get_market_snapshot(code)[1][["code","last_price","total_market_val"]]

    # print(market_snapshot)
    # print(type(market_snapshot))
    # market_snapshot.to_csv("market_snapshot.csv")

    # 4点以后执行，则最新价就是收盘价

    # 恒生指数最新价
    # hsi_last_price = quote_ctx.get_market_snapshot("HK.800000")[1]["last_price"].tolist()[0]
    # 国企指数最新价
    # hscei_last_price = quote_ctx.get_market_snapshot("HK.800100")[1]["last_price"].tolist()[0]
    # 电商及互联网板块指数最新价
    # internet_last_price = quote_ctx.get_market_snapshot("HK.BK1096")[1]["last_price"].tolist()[0]
    # print(internet_last_price)

    # print(hsi_last_price)
    # print(hscei_last_price)

    # 计算指标
    # 股票收盘价/恒生指数收盘价
    # market_snapshot["result"] = market_snapshot['last_price'].apply(lambda x: x / internet_last_price )

    # 排序-切片前四分位
    # result_len = (int)(len(market_snapshot) / 4)
    # sort_result = market_snapshot.sort_values(
    # by = ["result","total_market_val"], ascending = (False,False)).iloc[:result_len]

    # print(result_len)
