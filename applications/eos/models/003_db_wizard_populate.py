# from gluon.contrib.populate import populate

# if db(db.auth_user).isempty():
    # user1 = db.auth_user.insert(first_name='System', last_name='Admin', username='admin', email='admin@gmail.com', password='pbkdf2(1000,20,sha512)$87a2bde86b90bd73$d62cb18a1793aef9b8431b17dd196feb1ee800c9')
    # user2 = db.auth_user.insert(first_name='Nguyen Minh', last_name='Tuan', username='tuan', email='tuan@gmail.com', password='pbkdf2(1000,20,sha512)$87a2bde86b90bd73$d62cb18a1793aef9b8431b17dd196feb1ee800c9')

# # -------------------------------------------------------------------------
# if db(db.auth_group).isempty():
    # role1 = db.auth_group.insert(role='admin')
    # role2 = db.auth_group.insert(role='maintain')
    # role3 = db.auth_group.insert(role='managers')

# # -------------------------------------------------------------------------
# if db(db.auth_membership).isempty():
    # db.auth_membership.insert(user_id=user1.id, group_id=role1.id)
    # db.auth_membership.insert(user_id=user2.id, group_id=role1.id)
    
# if db(db.auth_permission).isempty():
    # pass
    
# #-------------------------------------------------    
# if db(db.usr).isempty():
    # usr1 = db.usr.insert(username='admin',
                  # password='pbkdf2(1000,20,sha512)$87a2bde86b90bd73$d62cb18a1793aef9b8431b17dd196feb1ee800c9', #password = '123123'
                  # firstname='Tuan (Admin)', lastname='Nguyen Minh', 
                  # email='admin@gmail.com')
    
# if db(db.provinces).isempty():
    # db.provinces.insert(province_name='An Giang', province_code='AG'          , order = 1)
    # db.provinces.insert(province_name='Bắc Cạn', province_code='BC'          , order = 2)
    # bd = db.provinces.insert(province_name='Bình Dương', province_code='BD'       , order = 3)
    # bdd = db.provinces.insert(province_name='Bình Ðịnh', province_code='BÐ'        , order = 4)
    # db.provinces.insert(province_name='Bắc Giang', province_code='BG'        , order = 5)
    # db.provinces.insert(province_name='Bạc Liêu', province_code='BL'         , order = 6)
    # bn = db.provinces.insert(province_name='Bắc Ninh', province_code='BN'         , order = 7)
    # db.provinces.insert(province_name='Bình Phước', province_code='BP'      , order = 8)
    # db.provinces.insert(province_name='Bến Tre', province_code='BT'          , order = 9)
    # db.provinces.insert(province_name='Bình Thuận', province_code='BTh'      , order = 10)
    # db.provinces.insert(province_name='Bà Rịa - Vũng Tàu', province_code='BV', order = 11)
    # db.provinces.insert(province_name='Cao Bằng', province_code='CB'         , order = 12)
    # db.provinces.insert(province_name='Cà Mau', province_code='CM'           , order = 13)
    # db.provinces.insert(province_name='Cần Thơ', province_code='CT'          , order = 14)
    # db.provinces.insert(province_name='Ðà Nẵng', province_code='ÐNa'         , order = 15)
    # db.provinces.insert(province_name='Ðắc Lắc', province_code='ÐL'          , order = 16)
    # db.provinces.insert(province_name='Ðắc Nông', province_code='ÐNô'        , order = 17)
    # db.provinces.insert(province_name='Ðiện Biên', province_code='ÐB'        , order = 18)
    # dnai = db.provinces.insert(province_name='Ðồng Nai', province_code='ÐN'         , order = 19)
    # db.provinces.insert(province_name='Ðồng Tháp', province_code='ÐT'        , order = 20)
    # db.provinces.insert(province_name='Gia Lai', province_code='GL'          , order = 21)
    # db.provinces.insert(province_name='Hà Giang', province_code='HG'         , order = 22)
    # hna = db.provinces.insert(province_name='Hà Nam', province_code='HNa'          , order = 23)
    # hn = db.provinces.insert(province_name='Hà Nội', province_code='HN'           , order = 24)
    # ht = db.provinces.insert(province_name='Hà Tĩnh', province_code='HT'          , order = 25)
    # db.provinces.insert(province_name='Hải Dưương', province_code='HD'       , order = 26)
    # db.provinces.insert(province_name='Hải Phòng', province_code='HP'        , order = 27)
    # db.provinces.insert(province_name='Hậu Giang', province_code='HGi'       , order = 28)
    # db.provinces.insert(province_name='Hoà Bình', province_code='HB'         , order = 29)
    # db.provinces.insert(province_name='Hưng Yên', province_code='HY'         , order = 30)
    # db.provinces.insert(province_name='Kiên Giang', province_code='KG'       , order = 31)
    # db.provinces.insert(province_name='Khánh Hoà', province_code='KH'        , order = 32)
    # db.provinces.insert(province_name='Kon Tum', province_code='KT'          , order = 33)
    # db.provinces.insert(province_name='Lai Châu', province_code='LC'         , order = 34)
    # db.provinces.insert(province_name='Lâm Ðồng', province_code='LÐ'         , order = 35)
    # db.provinces.insert(province_name='Lạng Sơn', province_code='LS'         , order = 36)
    # lca = db.provinces.insert(province_name='Lào Cai', province_code='LCa'         , order = 37)
    # db.provinces.insert(province_name='Long An', province_code='LA'          , order = 38)
    # db.provinces.insert(province_name='Nam Ðịnh', province_code='NÐ'         , order = 39)
    # na = db.provinces.insert(province_name='Nghệ An', province_code='NA'          , order = 40)
    # nb = db.provinces.insert(province_name='Ninh Bình', province_code='NB'        , order = 41)
    # db.provinces.insert(province_name='Ninh Thuận', province_code='NT'       , order = 42)
    # pt = db.provinces.insert(province_name='Phú Thọ', province_code='PT'          , order = 43)
    # db.provinces.insert(province_name='Phú Yên', province_code='PY'          , order = 44)
    # db.provinces.insert(province_name='Quảng Bình', province_code='QB'       , order = 45)
    # db.provinces.insert(province_name='Quảng Nam', province_code='QNa'       , order = 46)
    # db.provinces.insert(province_name='Quảng Ngãi', province_code='QNg'      , order = 47)
    # qn = db.provinces.insert(province_name='Quảng Ninh', province_code='QN'       , order = 48)
    # db.provinces.insert(province_name='Quảng Trị', province_code='QT'        , order = 49)
    # db.provinces.insert(province_name='Tp. Hồ Chí Minh', province_code='HCM'   , order = 50)
    # db.provinces.insert(province_name='Sơn La', province_code='SL'           , order = 51)
    # db.provinces.insert(province_name='Sóc Trăng', province_code='ST'        , order = 52)
    # db.provinces.insert(province_name='Tây Ninh', province_code='TN'         , order = 53)
    # db.provinces.insert(province_name='Thái Bình', province_code='TB'        , order = 54)
    # tng = db.provinces.insert(province_name='Thái Nguyên', province_code='TNg'     , order = 55)
    # db.provinces.insert(province_name='Thanh Hoá', province_code='TH'        , order = 56)
    # tth = db.provinces.insert(province_name='Thừa Thiên Huế', province_code='TTH'  , order = 57)
    # db.provinces.insert(province_name='Tiền Giang', province_code='TG'       , order = 58)
    # db.provinces.insert(province_name='Tuyên Quang', province_code='TQ'      , order = 59)
    # db.provinces.insert(province_name='Trà Vinh', province_code='TV'         , order = 60)
    # db.provinces.insert(province_name='Vĩnh Long', province_code='VL'        , order = 61)
    # db.provinces.insert(province_name='Vĩnh Phúc', province_code='VP'        , order = 62)
    # db.provinces.insert(province_name='Yên Bái', province_code='YB'          , order = 63)

# if db(db.indicators).isempty():
    # tss_0 = db.indicators.insert(indicator='TSS',   source_name='TSS',  unit='mg/l',    indicator_type=0, tendency_value=70, preparing_value=90, exceed_value=100)
    # tss_1 = db.indicators.insert(indicator='TSS',   source_name='TSS',  unit='mg/l',    indicator_type=1, tendency_value=70, preparing_value=90, exceed_value=100)
    # db.indicators.insert(indicator='FLOW',  source_name='FLOW', unit='m3/h',    indicator_type=0)
    # db.indicators.insert(indicator='Clo',   source_name='Clo',  unit='mg/l',    indicator_type=0)
    # db.indicators.insert(indicator='Clo',   source_name='Clo',  unit='mg/l',    indicator_type=1)
    # db.indicators.insert(indicator='COD',   source_name='COD',  unit='mg/l',    indicator_type=0)
    # cod_1 = db.indicators.insert(indicator='COD',   source_name='COD',  unit='mg/l',    indicator_type=1)
    # ph_0 = db.indicators.insert(indicator='pH',    source_name='pH',   unit='',        indicator_type=0, tendency_value=6.3, preparing_value=8.1, exceed_value=9)
    # ph_1 = db.indicators.insert(indicator='pH',    source_name='pH',   unit='', indicator_type=1, tendency_value=6.3, preparing_value=8.1, exceed_value=9)
    # db.indicators.insert(indicator='COLOR', source_name='COLOR', unit='Pt-Co',  indicator_type=0)
    # db.indicators.insert(indicator='Cu',    source_name='Cu',   unit='mg/l',    indicator_type=0)
    # temp_0 = db.indicators.insert(indicator='Temp',  source_name='Temp', unit='oC',      indicator_type=0, tendency_value=28, preparing_value=36, exceed_value=40)
    # temp_1 = db.indicators.insert(indicator='Temp',  source_name='Temp', unit='oC',      indicator_type=1, tendency_value=28, preparing_value=36, exceed_value=40)
    # db.indicators.insert(indicator='Temp',  source_name='Temp', unit='oC',      indicator_type=2, tendency_value=28, preparing_value=36, exceed_value=40)
    # db.indicators.insert(indicator='Temp',  source_name='Temp', unit='oC',      indicator_type=3)
    # temp_4 = db.indicators.insert(indicator='Temp',  source_name='Temp', unit='oC',      indicator_type=4)
    # db.indicators.insert(indicator='Amoni', source_name='Amoni', unit='mg/l',   indicator_type=0)
    # db.indicators.insert(indicator='Amoni', source_name='Amoni', unit='mg/l',   indicator_type=1)
    # db.indicators.insert(indicator='Dust',  source_name='Dust', unit='mg/Nm3',  indicator_type=3, tendency_value=84, preparing_value=108, exceed_value=120)
    # nox_3 = db.indicators.insert(indicator='NOx',   source_name='NOx',  unit='mg/Nm3',  indicator_type=3, tendency_value=273, preparing_value=351, exceed_value=390)
    # nox_4 = db.indicators.insert(indicator='NOx',   source_name='NOx',  unit='mg/Nm3',  indicator_type=4, tendency_value=273, preparing_value=351, exceed_value=390)
    # db.indicators.insert(indicator='O2',    source_name='O2',   unit='%',       indicator_type=3, tendency_value=4.2, preparing_value=5.4, exceed_value=6)
    # o2_1 = db.indicators.insert(indicator='O2',    source_name='O2',   unit='%',       indicator_type=1)
    # so2_3 = db.indicators.insert(indicator='SO2',   source_name='SO2',  unit='mg/Nm3',  indicator_type=3, tendency_value=245, preparing_value=315, exceed_value=350)
    # so2_4 = db.indicators.insert(indicator='SO2',   source_name='SO2',  unit='mg/Nm3',  indicator_type=4, tendency_value=245, preparing_value=315, exceed_value=350)
    # o3_4 = db.indicators.insert(indicator='O3',    source_name='O3',   unit='µg/m3',   indicator_type=4)
    # pm10_4 = db.indicators.insert(indicator='PM10',  source_name='PM10', unit='µg/m3',   indicator_type=4)
    # db.indicators.insert(indicator='PM2.5', source_name='PM2.5', unit='µg/m3',  indicator_type=4)
    # no_3 = db.indicators.insert(indicator='NO',    source_name='NO',   unit='µg/m3',   indicator_type=3)
    # no_4 = db.indicators.insert(indicator='NO',    source_name='NO',   unit='µg/m3',   indicator_type=4)
    # no2_3 = db.indicators.insert(indicator='NO2',   source_name='NO2',  unit='µg/m3',   indicator_type=3)
    # no2_4 = db.indicators.insert(indicator='NO2',   source_name='NO2',  unit='µg/m3',   indicator_type=4)
    # tsp_4 = db.indicators.insert(indicator='TSP',   source_name='TSP',  unit='µg/m3',   indicator_type=4)
    # db.indicators.insert(indicator='Fe',    source_name='Fe',   unit='mg/l',    indicator_type=0)
    # db.indicators.insert(indicator='Zn',    source_name='Zn',   unit='mg/l',    indicator_type=0)
    # db.indicators.insert(indicator='Xyanua', source_name='Xyanua', unit='mg/l', indicator_type=0)
    # db.indicators.insert(indicator='Oil',   source_name='Oil',  unit='mg/l',    indicator_type=0)
    # do_0 = db.indicators.insert(indicator='DO',    source_name='DO',   unit='mg/l',    indicator_type=0)
    # do_1 = db.indicators.insert(indicator='DO',    source_name='DO',   unit='mg/l',    indicator_type=1)
    # db.indicators.insert(indicator='BOD',   source_name='BOD',  unit='mg/l',    indicator_type=1)
    # co_4 = db.indicators.insert(indicator='CO',    source_name='CO',   unit='µg/m3',   indicator_type=4)
    # ec_0 = db.indicators.insert(indicator='EC',    source_name='EC',   unit='mS/cm',   indicator_type=0)
    # ec_1 = db.indicators.insert(indicator='EC',    source_name='EC',   unit='mS/cm',   indicator_type=1)
    # hg_1 = db.indicators.insert(indicator='HG',    source_name='HG',   unit='mg/l',    indicator_type=1)
    # orp_1 = db.indicators.insert(indicator='ORP',   source_name='ORP',  unit='mv',      indicator_type=1)
    # orp_0 = db.indicators.insert(indicator='ORP',   source_name='ORP',  unit='mv',      indicator_type=0)
    # toc_1 = db.indicators.insert(indicator='TOC',   source_name='TOC',  unit='',        indicator_type=1)
    # tn_1 = db.indicators.insert(indicator='TN',    source_name='TN',   unit='mg/l',    indicator_type=1)    # Tong P
    # tp_1 = db.indicators.insert(indicator='TP',    source_name='TP',   unit='mg/l',    indicator_type=1)    # Tong N
    # tc_1 = db.indicators.insert(indicator='TC',    source_name='TC',   unit='mg/l',    indicator_type=1)    # Tong C
    # db.indicators.insert(indicator='Nitrate',           source_name='Nitrate',          unit='mg/l',    indicator_type=1, tendency_value=49, preparing_value=63, exceed_value=70)
    # db.indicators.insert(indicator='Turbidity',         source_name='Turbidity',        unit='NTU',     indicator_type=1)
    # db.indicators.insert(indicator='Coliform',         source_name='Coliform',        unit='MPN/100ml',     indicator_type=1)
    # db.indicators.insert(indicator='N-NH4',         source_name='N-NH4',        unit='mg/l',     indicator_type=1)
    # db.indicators.insert(indicator='P-PO4',         source_name='P-PO4',        unit='mg/l',     indicator_type=1)
    # db.indicators.insert(indicator='Temp Enviroment',   source_name='Temp Enviroment',  unit='oC',      indicator_type=2)
    # db.indicators.insert(indicator='Water Level',       source_name='Water Level',      unit='m',       indicator_type=2)
    # db.indicators.insert(indicator='Salinity',          source_name='Salinity',         unit='‰',       indicator_type=2)
    # thc_4 = db.indicators.insert(indicator='THC',   source_name='THC',  unit='ppmC',    indicator_type=4)
    # pb_4 = db.indicators.insert(indicator='Pb',   source_name='Pb',  unit='',    indicator_type=4)
    
# if db(db.areas).isempty():
    # area_sc = db.areas.insert(area_code = 'LVSC', area_name = 'Lưu Vực Sông Cầu', order = 1, description = 'Thái Nguyên, Bắc Cạn, Vĩnh Phúc, Bắc Giang, Bắc Ninh, Hải Dương.')
    # area_nd = db.areas.insert(area_code = 'LVSN-Đ', area_name = 'Lưu Vực Sông Nhuệ - Đáy', order = 2, description = 'Hà Nội, Hà Nam, Nam Định, Ninh Bình')
    # area_dn = db.areas.insert(area_code = 'LVSĐN', area_name = 'Lưu Vực Sông Đồng Nai', order = 3, description = 'Tp.Hồ Chí Minh, Đồng Nai, Bình Dương, Bình Phước, Bà Rịa - Vũng Tầu, Lâm Đồng, Đắc Lắc, Đắc Nông, Ninh Thuận, Bình Thuận, Tây Ninh, Long An')

# if db(db.stations).isempty():
    # # db.stations.insert(station_name='', station_type=, longitude=, latitude=, province_id= )
    # st_cg = db.stations.insert(station_name='Cam Giá',      station_type=0, station_code='', longitude=21.567654, latitude=105.870552, province_id=tng.id, status=0, area_id = area_sc.id )
    # st_yb = db.stations.insert(station_name='Yên Bình',     station_type=0, station_code='', longitude=21.431113, latitude=105.900894, province_id=tng.id, status=0, area_id = area_sc.id )
    # st_hmac = db.stations.insert(station_name='Hòa Mạc',    station_type=0, station_code='', longitude=20.630036, latitude=105.994200, province_id=tng.id, status=1, area_id = area_nd.id )
    # st_fomosa = db.stations.insert(station_name='Formosa Hà Tĩnh',     station_type=0, station_code='', longitude=18.0293109, latitude=106.4014164, province_id=ht.id, status=1, area_id = area_sc.id )
    # st_sstn = db.stations.insert(station_name='SamSung - Thái Nguyên', station_type=0, station_code='SSTN', longitude=21.4277371, latitude=105.8934791, province_id=tng.id, status=0, area_id = area_sc.id )
    # st_ntub = db.stations.insert(station_name='Uông Bí',    station_type=0, station_code='NTUB', longitude=21.0331246, latitude=106.7780982, province_id=qn.id, status=0, area_id = area_sc.id )
    # st_ntbd = db.stations.insert(station_name='Bình Định',  station_type=0, station_code='NTBD', longitude=10.605688, latitude=107.036674, province_id=bdd.id, status=0, area_id = area_dn.id )
    # st_lt = db.stations.insert(station_name='Long Thành',   station_type=1, station_code='', longitude=10.7774345, latitude=106.9248486, province_id=dnai.id, status=2, area_id = area_dn.id )
    # st_nmnb = db.stations.insert(station_name='Ninh Bình',  station_type=1, station_code='NMNB', longitude=20.454169, latitude=105.881901, province_id=nb.id, status=2, area_id = area_sc.id )
    # st_nmbn = db.stations.insert(station_name='Bắc Ninh',   station_type=1, station_code='NMBN', longitude=21.1740036, latitude=106.0075952, province_id=bn.id, status=1, area_id = area_sc.id )
    # st_nmbh = db.stations.insert(station_name='Biên Hòa',   station_type=1, station_code='NMBH', longitude=10.9141177, latitude=106.8041007, province_id=dnai.id, status=1, area_id = area_dn.id )
    # st_nmcp = db.stations.insert(station_name='Cẩm Phả',    station_type=1, station_code='NMCP', longitude=21.0810968, latitude=107.1493817, province_id=qn.id, status=0, area_id = area_nd.id )
    # st_nmhl = db.stations.insert(station_name='Hạ Long',    station_type=1, station_code='NMHL', longitude=20.9673211, latitude=106.9027864, province_id=qn.id, status=0, area_id = area_sc.id )
    # st_nmhna = db.stations.insert(station_name='Hà Nam',    station_type=1, station_code='NMHNA',longitude=20.5506433, latitude=105.912159, province_id=hna.id, status=0, area_id = area_nd.id )
    # st_nmbd = db.stations.insert(station_name='Bình Dương', station_type=1, station_code='NMBD', longitude=10.562859, latitude=107.032416, province_id=bd.id, status=0, area_id = area_dn.id )
    # db.stations.insert(station_name='Tà Lài',               station_type=1, station_code='', longitude=11.3637516, latitude=107.3278419, province_id=dnai.id, status=2, area_id = area_sc.id )
    # st_cn = db.stations.insert(station_name='Cao Ngạn',              station_type=3, station_code='', longitude=21.612537, latitude=105.81464, province_id=tng.id, status=3, area_id = area_sc.id )
    # st_ld = db.stations.insert(station_name='Luyện Đồng',            station_type=3, station_code='', longitude=22.305083, latitude=104.131938, province_id=lca.id, status=3, area_id = area_sc.id )
    # st_pt = db.stations.insert(station_name='Trạm khí Phú Thọ',      station_type=4, station_code='TTT', longitude=21.317282, latitude=104.5747232, province_id=pt.id, status=0, is_qi = True, area_id = area_sc.id )
    # st_hn = db.stations.insert(station_name='Trạm khí Nguyễn Văn Cừ',station_type=4, station_code='NVCU', longitude=21.0429234, latitude=105.8690654, province_id=hn.id, status=0, is_qi = True, area_id = area_nd.id )
    # st_hue = db.stations.insert(station_name='Trạm khí Huế',         station_type=4, station_code='TQT', longitude=16.4533788, latitude=107.5070723, province_id=tth.id, status=0, is_qi = True, area_id = area_sc.id )
    # st_hm = db.stations.insert(station_name='Hoàng Mai',             station_type=4, station_code='HM', longitude=20.974852, latitude=105.8229188, province_id=hn.id, status=0, is_qi = True, area_id = area_nd.id )
    # st_nb = db.stations.insert(station_name='Ninh Bình',             station_type=4, station_code='NB', longitude=20.245116, latitude=105.9404319, province_id=nb.id, status=0, is_qi = True, area_id = area_sc.id )
    # st_ub = db.stations.insert(station_name='Uông Bí',               station_type=4, station_code='UB', longitude=20.245116, latitude=105.9404319, province_id=qn.id, status=0, is_qi = True, area_id = area_nd.id )
    # st_v = db.stations.insert(station_name='Vinh',                   station_type=4, station_code='VINH', longitude=18.7037078, latitude=105.6269437, province_id=na.id, status=0, is_qi = True, area_id = area_sc.id )
    
    # st_k_qn = db.stations.insert(station_name='Quảng Ninh',          station_type=4, station_code='KHI_QN', longitude=20.945834, latitude=107.109159, province_id=qn.id, status=0, area_id = area_sc.id )
    # st_k_mk = db.stations.insert(station_name='Mạo Khê',             station_type=4, station_code='KHI_MK', longitude=21.064437, latitude=106.599365, province_id=qn.id, status=0, area_id = area_nd.id )
    # st_k_nct = db.stations.insert(station_name='Nam Cầu Trắng',      station_type=4, station_code='KHI_NCT',longitude=20.968252, latitude=107.159152, province_id=qn.id, status=4, area_id = area_nd.id, off_time = request.now )
    # st_k_qh = db.stations.insert(station_name='Quang Hanh',          station_type=4, station_code='KHI_QH',longitude=21.009555, latitude=107.232036, province_id=qn.id, status=4, area_id = area_sc.id, off_time = request.now )
    # st_k_pn = db.stations.insert(station_name='Uông Bí - Phương Nam',station_type=4, station_code='KHI_PN',longitude=21.017557, latitude=106.696966, province_id=qn.id, status=5, area_id = area_nd.id, off_time = request.now )
    # st_k_kc = db.stations.insert(station_name='Khe Chàm',            station_type=4, station_code='KHI_KC',longitude=21.065241, latitude=107.325674, province_id=qn.id, status=5, area_id = area_sc.id, off_time = request.now )
# else:
    # st_k_qn =   db((db.stations.station_name == 'Quảng Ninh') & (db.stations.station_type==4)).select().first()
    # st_k_mk =   db((db.stations.station_name == 'Mạo Khê') & (db.stations.station_type==4)).select().first()
    # st_k_nct =   db((db.stations.station_name == 'Nam Cầu Trắng') & (db.stations.station_type==4)).select().first()
    # st_k_qh =   db((db.stations.station_name == 'Quang Hanh') & (db.stations.station_type==4)).select().first()
    # st_k_pn =   db((db.stations.station_name == 'Uông Bí - Phương Nam') & (db.stations.station_type==4)).select().first()
    # st_k_kc =   db((db.stations.station_name == 'Khe Chàm') & (db.stations.station_type==4)).select().first()
    
    
    # st_cg =     db((db.stations.station_name == 'Cam Giá') & (db.stations.station_type==0)).select().first()
    # st_yb =     db((db.stations.station_name == 'Yên Bình') & (db.stations.station_type==0)).select().first()
    # st_hmac =   db((db.stations.station_name == 'Hòa Mạc') & (db.stations.station_type==0)).select().first()
    # st_fomosa = db((db.stations.station_name == 'Formosa Hà Tĩnh') & (db.stations.station_type==0)).select().first()
    # st_sstn =   db((db.stations.station_name == 'SamSung - Thái Nguyên') & (db.stations.station_type==0)).select().first()
    # st_ntub =   db((db.stations.station_name == 'Uông Bí') & (db.stations.station_type==0)).select().first()
    # st_ntbd =   db((db.stations.station_name == 'Bình Định') & (db.stations.station_type==0)).select().first()
    
    # st_lt =     db((db.stations.station_name == 'Long Thành') & (db.stations.station_type==1)).select().first()
    # st_nmnb =   db((db.stations.station_name == 'Ninh Bình') & (db.stations.station_type==1)).select().first()
    # st_nmbn =   db((db.stations.station_name == 'Bắc Ninh') & (db.stations.station_type==1)).select().first()
    # st_nmbh =   db((db.stations.station_name == 'Biên Hòa') & (db.stations.station_type==1)).select().first()
    # st_nmcp =   db((db.stations.station_name == 'Cẩm Phả') & (db.stations.station_type==1)).select().first()
    # st_nmhl =   db((db.stations.station_name == 'Hạ Long') & (db.stations.station_type==1)).select().first()
    # st_nmhna =  db((db.stations.station_name == 'Hà Nam') & (db.stations.station_type==1)).select().first()
    # st_nmbd =   db((db.stations.station_name == 'Bình Dương') & (db.stations.station_type==1)).select().first()
    
    # st_cn =     db((db.stations.station_name == 'Cao Ngạn') & (db.stations.station_type==3)).select().first()
    # st_ld =     db((db.stations.station_name == 'Luyện Đồng') & (db.stations.station_type==3)).select().first()
    # st_pt =     db((db.stations.station_name == 'Trạm khí Phú Thọ') & (db.stations.station_type==4)).select().first()
    # st_hn =     db((db.stations.station_name == 'Trạm khí Nguyễn Văn Cừ') & (db.stations.station_type==4)).select().first()
    # st_hue =    db((db.stations.station_name == 'Trạm khí Huế') & (db.stations.station_type==4)).select().first()
    # st_hm =     db((db.stations.station_name == 'Hoàng Mai') & (db.stations.station_type==4)).select().first()
    # st_nb =     db((db.stations.station_name == 'Ninh Bình') & (db.stations.station_type==4)).select().first()
    # st_ub =     db((db.stations.station_name == 'Uông Bí') & (db.stations.station_type==4)).select().first()
    # st_v =      db((db.stations.station_name == 'Vinh') & (db.stations.station_type==4)).select().first()
    
# if db(db.camera_links).isempty():   # Ca camera va station_alarm
    # import random
    # from datetime import datetime, timedelta
    # sts = db(db.stations.id > 0).select(db.stations.id, db.stations.station_type, db.stations.station_name)
    # for item in sts:
        # # Camera
        # db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST6.stream/playlist.m3u8')
        # db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST7.stream/playlist.m3u8')
        # db.camera_links.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type, camera_source = 'http://27.118.20.209:1935/CAM/CAMTEST8.stream/playlist.m3u8')

        # # Alarm info
        # db.station_alarm.insert(station_id = item.id, station_name = item.station_name, station_type = item.station_type,
            # tendency_method_email = True, preparing_method_email = True, exceed_method_email = True,
            # tendency_email_list = 'mail1@test.com, mail2@test.com, mail2@test.com, mail3@test.com', 
            # preparing_email_list = 'mail1@test.com, mail2@test.com, mail2@test.com, mail3@test.com',
            # exceed_email_list = 'mail1@test.com, mail2@test.com, mail2@test.com, mail3@test.com',
            # tendency_msg = 'Lỗi không có thông tin tram',
            # preparing_msg = 'Lỗi không có thông tin tram',
            # exceed_msg = 'Lỗi không có thông tin tram',
        # )
        
        # # Equipment
        # indi = ['pH', 'COD', 'Temperature', 'SO2', 'NOx', 'O3', 'Nitrate', 'TSS', 'CO', 'DO', 'EC', 'ORP', 'PM10', 'PM2.5', 'NO2']
        # brand = ['Toshiba Nhật', 'Siemens Đức', 'E-Sensor Mỹ', 'K-Sensor Hàn Quốc', 'Hitachi Nhật']
        # madein = ['Nhật', 'Đức', 'Mỹ', 'Hàn Quốc', 'Pháp', 'Italia', 'Trung Quốc']
        # db.equipments.insert(station_id = item.id, station_name = item.station_name, 
            # equipment = 'Thiết bị (sensor) đo chỉ số %s' % indi[random.randint(0, len(indi) - 1)],
            # brandname = brand[random.randint(0, len(brand) - 1)], made_in = madein[random.randint(0, len(madein) - 1)],
            # start_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_start = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_end = datetime.now() + timedelta(days=random.randint(0, 1000)),
            # implement_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # produce_date = datetime.now() - timedelta(days=random.randint(-200, -100)),
            # lrv = random.randint(0, 100), urv = random.randint(0, 100)
        # )
        # db.equipments.insert(station_id = item.id, station_name = item.station_name, 
            # equipment = 'Thiết bị (sensor) đo chỉ số %s' % indi[random.randint(0, len(indi) - 1)],
            # brandname = brand[random.randint(0, len(brand) - 1)], made_in = madein[random.randint(0, len(madein) - 1)],
            # start_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_start = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_end = datetime.now() + timedelta(days=random.randint(0, 1000)),
            # implement_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # produce_date = datetime.now() - timedelta(days=random.randint(-200, -100)),
            # lrv = random.randint(0, 100), urv = random.randint(0, 100)
        # )
        # db.equipments.insert(station_id = item.id, station_name = item.station_name, 
            # equipment = 'Thiết bị (sensor) đo chỉ số %s' % indi[random.randint(0, len(indi) - 1)],
            # brandname = brand[random.randint(0, len(brand) - 1)], made_in = madein[random.randint(0, len(madein) - 1)],
            # start_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_start = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_end = datetime.now() + timedelta(days=random.randint(0, 1000)),
            # implement_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # produce_date = datetime.now() - timedelta(days=random.randint(-200, -100)),
            # lrv = random.randint(0, 100), urv = random.randint(0, 100)
        # )
        # db.equipments.insert(station_id = item.id, station_name = item.station_name, 
            # equipment = 'Thiết bị (sensor) đo chỉ số %s' % indi[random.randint(0, len(indi) - 1)],
            # brandname = brand[random.randint(0, len(brand) - 1)], made_in = madein[random.randint(0, len(madein) - 1)],
            # start_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_start = datetime.now() - timedelta(days=random.randint(0, 100)),
            # warranty_end = datetime.now() + timedelta(days=random.randint(0, 1000)),
            # implement_date = datetime.now() - timedelta(days=random.randint(0, 100)),
            # produce_date = datetime.now() - timedelta(days=random.randint(-200, -100)),
            # lrv = random.randint(0, 100), urv = random.randint(0, 100)
        # )

# if db(db.station_indicator).isempty():
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_kc.id, station_name='Khe Chàm', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_pn.id, station_name='Uông Bí - Phương Nam', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_qn.id, station_name='Quảng Ninh', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_k_mk.id, station_name='Mạo Khê', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_ld.id, station_name='Luyện Đồng', station_type=3, indicator_id=nox_3.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_ld.id, station_name='Luyện Đồng', station_type=3, indicator_id=no_3.id,  exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_ld.id, station_name='Luyện Đồng', station_type=3, indicator_id=no2_3.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_ld.id, station_name='Luyện Đồng', station_type=3, indicator_id=so2_3.id, exceed_value=350, unit='mg/Nm3')
    
    # db.station_indicator.insert(station_id = st_cn.id, station_name='Cao Ngạn', station_type=3, indicator_id=nox_3.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_cn.id, station_name='Cao Ngạn', station_type=3, indicator_id=no_3.id,  exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_cn.id, station_name='Cao Ngạn', station_type=3, indicator_id=no2_3.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_cn.id, station_name='Cao Ngạn', station_type=3, indicator_id=so2_3.id, exceed_value=350, unit='mg/Nm3')
    
    # db.station_indicator.insert(station_id = st_lt.id, station_name='Long Thành', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_lt.id, station_name='Long Thành', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_lt.id, station_name='Long Thành', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    
    # db.station_indicator.insert(station_id = st_fomosa.id, station_name='Formosa Hà Tĩnh', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_fomosa.id, station_name='Formosa Hà Tĩnh', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_fomosa.id, station_name='Formosa Hà Tĩnh', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_fomosa.id, station_name='Formosa Hà Tĩnh', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_hmac.id, station_name='Hòa Mạc', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_hmac.id, station_name='Hòa Mạc', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_hmac.id, station_name='Hòa Mạc', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_hmac.id, station_name='Hòa Mạc', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_yb.id, station_name='Yên Bình', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_yb.id, station_name='Yên Bình', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_yb.id, station_name='Yên Bình', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_yb.id, station_name='Yên Bình', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_cg.id, station_name='Cam Giá', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_cg.id, station_name='Cam Giá', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_cg.id, station_name='Cam Giá', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_cg.id, station_name='Cam Giá', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=do_0.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_ntbd.id, station_name='Bình Định', station_type=0, indicator_id=ec_0.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=do_0.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_ntub.id, station_name='Uông Bí', station_type=0, indicator_id=ec_0.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=ph_0.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=orp_0.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=temp_0.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=tss_0.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=do_0.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_sstn.id, station_name='SamSung - Thái Nguyên', station_type=0, indicator_id=ec_0.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=do_1.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbd.id, station_name='Bình Dương', station_type=1, indicator_id=ec_1.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=do_1.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=ec_1.id, exceed_value=480, unit='mS/cm')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=toc_1.id, exceed_value=110, unit='')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=tn_1.id, exceed_value=100, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmhna.id, station_name='Hà Nam', station_type=1, indicator_id=tp_1.id, exceed_value=90, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_nmhl.id, station_name='Hạ Long', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmhl.id, station_name='Hạ Long', station_type=1, indicator_id=o2_1.id, exceed_value=1.2, unit='%')
    # db.station_indicator.insert(station_id = st_nmhl.id, station_name='Hạ Long', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmhl.id, station_name='Hạ Long', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=o2_1.id, exceed_value=1.2, unit='%')
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=cod_1.id, exceed_value=100, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmcp.id, station_name='Cẩm Phả', station_type=1, indicator_id=toc_1.id, exceed_value=110, unit='')
    
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=do_1.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbh.id, station_name='Biên Hòa', station_type=1, indicator_id=ec_1.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=do_1.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmbn.id, station_name='Bắc Ninh', station_type=1, indicator_id=ec_1.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=ph_1.id, exceed_value=9, unit='')
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=orp_1.id, exceed_value=270, unit='mv')
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=temp_1.id, exceed_value=29, unit='oC')
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=tss_1.id, exceed_value=33, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=do_1.id, exceed_value=10, unit='mg/l')
    # db.station_indicator.insert(station_id = st_nmnb.id, station_name='Ninh Bình', station_type=1, indicator_id=ec_1.id, exceed_value=480, unit='mS/cm')
    
    # db.station_indicator.insert(station_id = st_v.id, station_name='Vinh', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_v.id, station_name='Vinh', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_v.id, station_name='Vinh', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_v.id, station_name='Vinh', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_ub.id, station_name='Uông Bí', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=pm10_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_nb.id, station_name='Ninh Bình', station_type=4, indicator_id=temp_4.id, exceed_value=30, unit='oC')
    
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hm.id, station_name='Hoàng Mai', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=o3_4.id, exceed_value=50, unit='µg/m3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=so2_4.id, exceed_value=350, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=co_4.id, exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=nox_4.id, exceed_value=390, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=no_4.id, exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')
    
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=no_4.id,  exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=nox_4.id, exceed_value=21, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=so2_4.id, exceed_value=59, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=co_4.id,  exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=o3_4.id,  exceed_value=50, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, indicator_id=thc_4.id, exceed_value=4, unit='ppmC')

    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=no_4.id,  exceed_value=4, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=no2_4.id, exceed_value=17, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=nox_4.id, exceed_value=21, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=so2_4.id, exceed_value=59, unit='mg/Nm3')
    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=co_4.id,  exceed_value=1800, unit='ug/m3')
    # db.station_indicator.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, indicator_id=o3_4.id,  exceed_value=50, unit='ug/m3')
    
# if db(db.aqi_indicators).isempty():    
    # db.aqi_indicators.insert(indicator_id = so2_4.id, indicator='SO2',  qc_1h = 350,   qc_3h = None,  qc_24h = 125,  qc_1y = 50)
    # db.aqi_indicators.insert(indicator_id =  co_4.id, indicator='CO',   qc_1h = 30000, qc_3h = 10000, qc_24h = 5000, qc_1y = None)
    # db.aqi_indicators.insert(indicator_id = nox_4.id, indicator='NOx',  qc_1h = 200,   qc_3h = None,  qc_24h = 100,  qc_1y = 40)
    # db.aqi_indicators.insert(indicator_id =  o3_4.id, indicator='O3',   qc_1h = 180,   qc_3h = 120,   qc_24h = 80,   qc_1y = None)
    # db.aqi_indicators.insert(indicator_id = tsp_4.id, indicator='TSP',  qc_1h = 300,   qc_3h = None,  qc_24h = 200,  qc_1y = 140)
    # db.aqi_indicators.insert(indicator_id = pm10_4.id,indicator='PM10', qc_1h = 300,   qc_3h = None,  qc_24h = 150,  qc_1y = 50)      # Lay theo gtri TSP 1h 
    # db.aqi_indicators.insert(indicator_id = pb_4.id,  indicator='Pb',   qc_1h = None,  qc_3h = None,  qc_24h = 1.5,  qc_1y = 0.5)      
    
# if db(db.station_types).isempty():
    # db.station_types.insert(station_type = 'Waste water')
    # db.station_types.insert(station_type = 'Surface water')
    # db.station_types.insert(station_type = 'Underground water')
    # db.station_types.insert(station_type = 'Stack emission')
    # db.station_types.insert(station_type = 'Ambient air')

# if db(db.agents).isempty():
    # db.agents.insert(agent_name = 'Bộ Tài Nguyên & Môi Trường', manage_agent = '', )

# ######### Dummy data ############################################################
# if db(db.station_off_log).isempty():  
    # from datetime import datetime, date, timedelta
    # db.station_off_log.insert(station_id = st_k_nct.id, station_name='Nam Cầu Trắng', station_type=4, province_id=qn.id, start_off=request.now)
    # db.station_off_log.insert(station_id = st_k_qh.id, station_name='Quang Hanh', station_type=4, province_id=qn.id, start_off=request.now)
    # db.station_off_log.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, province_id=tth.id, start_off=request.now - timedelta(seconds = 50000), end_off = request.now + timedelta(seconds = 50000), duration = 100000)
    # db.station_off_log.insert(station_id = st_hue.id, station_name='Trạm khí Huế', station_type=4, province_id=tth.id, start_off=request.now - timedelta(seconds = 200000), end_off = request.now - timedelta(seconds = 100000), duration = 100000)
    # db.station_off_log.insert(station_id = st_pt.id, station_name='Trạm khí Phú Thọ', station_type=4, province_id=pt.id, start_off=request.now, end_off = request.now +  timedelta(seconds = 36000), duration = 36000)
    # db.station_off_log.insert(station_id = st_hn.id, station_name='Trạm khí Nguyễn Văn Cừ', station_type=4, province_id=hn.id, start_off=request.now - timedelta(seconds = 36000), end_off = request.now + timedelta(seconds = 36000), duration = 72000)
    
# if db(db.notifications).isempty():    
    # db.notifications.insert(title='Trạm Formusa chỉ số pH vượt ngưỡng', sender=user1.id , receivers=[user1.id,user2.id,'3'], content='Hello guys! \n Trạm Formusa chỉ số pH vượt ngưỡng')    
    # db.notifications.insert(title='Trạm khí Phú Thọ chỉ số CO2 vượt ngưỡng', sender=user1.id , receivers=[user1.id,user2.id], content='Hello guys! \n Trạm khí Phú Thọ chỉ số CO2 vượt ngưỡng', notify_level = 1)    
    # db.notifications.insert(title='Trạm khí Phú Thọ chỉ số SO2 sắp vượt ngưỡng', sender=user1.id , receivers=[user1.id], content='Hello guys! \n Trạm khí Phú Thọ chỉ số SO2 sắp vượt ngưỡng', notify_level = 2)    
    
# from gluon.contrib.populate import populate    

# if db(db.commands_schedule).isempty():
    # populate(db.commands_schedule,10)
    
# if db(db.command_results).isempty():
    # # populate(db.command_results,5)
    # db.command_results.insert(command_schedule_id='command_schedule_id', command_id='command_id', station_id='station_id', station_name='station_name1', title='title', results={'CO':1.00,'CO2':2.00,'SO2':3.00})
    # db.command_results.insert(command_schedule_id='command_schedule_id', command_id='command_id', station_id='station_id', station_name='station_name2', title='title', results={'NO':1.00,'pH':2.00,'NOx':3.00})
    # db.command_results.insert(command_schedule_id='command_schedule_id', command_id='command_id', station_id='station_id', station_name='station_name3', title='title', results={'NO2':1.00,'O3':2.00,'SO2':3.00})
    # db.command_results.insert(command_schedule_id='command_schedule_id', command_id='command_id', station_id='station_id', station_name='station_name4', title='title', results={'CO':1.00,'CO2':2.00,'CO3':3.00,'CO4':4.00,'CO5':5.00,'CO6':6.00})
    # db.command_results.insert(command_schedule_id='command_schedule_id', command_id='command_id', station_id='station_id', station_name='station_name5', title='title', results={'CO':1.00,'CO2':2.00,'CO3':3.00,'CO4':4.00,'CO5':5.00,'CO6':6.00,'CO7':7.00})
        
# if db(db.alarm_logs).isempty():
    # populate(db.alarm_logs,10)

# if db(db.commands).isempty():
    # populate(db.commands,10)

# if db(db.station_off_log).isempty():
    # populate(db.station_off_log,10)
  
# if db(db.adjustments).isempty():
    # populate(db.adjustments,15)



# if db(db.qcvn).isempty():
    # st_1 = db.qcvn.insert(qcvn_code='QCVN 11-MT:2015/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải chăn nuôi', qcvn_subject='', qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=0)
    # st_2 = db.qcvn.insert(qcvn_code='QCVN 62-MT:2016/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải công nghiệp chế biến thuỷ sản', qcvn_subject='', qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=0)
    # st_3 = db.qcvn.insert(qcvn_code='QCVN 01-MT:2015/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải sơ chế cao su thiên nhiên', qcvn_subject='', qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=1 )
    # st_4 = db.qcvn.insert(qcvn_code='QCVN 12-MT:2015/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải công nghiệp giấy và bột giấy', qcvn_subject='',  qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=1)
    # st_5 = db.qcvn.insert(qcvn_code='QCVN 13-MT:2015/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải công nghiệp dệt nhuộm ', qcvn_subject='SSTN',  qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=0)
    # st_6 = db.qcvn.insert(qcvn_code='QCVN 40:2011/BTNMT',qcvn_type = 0, qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải công nghiệp', qcvn_subject='NTUB',  qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=0)
    # st_7 = db.qcvn.insert(qcvn_code='QCVN 29:2010/BTNMT',qcvn_type = 0,  qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải của kho và cửa hàng xăng dầu', qcvn_subject='NTBD',  qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=0)
    # st_8 = db.qcvn.insert(qcvn_code='QCVN 28:2010/BTNMT', qcvn_type = 0,  qcvn_name='Quy chuẩn kỹ thuật quốc gia về nước thải y tế', qcvn_subject='',  qcvn_description = 'Bộ tiêu chuẩn Việt Nam QCVN về nước thải', qcvn_priority=2)

# if db(db.qcvn_detail).isempty():
    # no_1 =   db(db.indicators.indicator == 'TSS').select().first()
    # no_2 =   db(db.indicators.indicator == 'Clo').select().first()
    # no_3 =   db(db.indicators.indicator == 'COD').select().first()
    # no_4 =   db(db.indicators.indicator == 'pH').select().first()
    # no_5 =   db(db.indicators.indicator == 'Amoni').select().first()
    # no_6 =   db(db.indicators.indicator == 'Dust').select().first()
    # no_7 =   db(db.indicators.indicator == 'NOx').select().first()
    # no_8 =   db(db.indicators.indicator == 'O2').select().first()
    # no_9 =   db(db.indicators.indicator == 'SO2').select().first()
    
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_1.id,  exceed_value=4, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_2.id, exceed_value=17, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_3.id, exceed_value=21, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_4.id, exceed_value=59, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_5.id,  exceed_value=1800, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_6.id,  exceed_value=50, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_1.id, qcvn_code ='QCVN 11-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_7.id,  exceed_value=50, unit='ug/m3')
                 
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_1.id, exceed_value=9, unit='')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_2.id, exceed_value=270, unit='mv')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_3.id, exceed_value=29, unit='oC')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_4.id, exceed_value=33, unit='mg/l')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_5.id, exceed_value=10, unit='mg/l')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_6.id, exceed_value=480, unit='mS/cm')
    # db.qcvn_detail.insert(qcvn_id = st_2.id, qcvn_code ='QCVN 62-MT:2016/BTNMT',qcvn_type=0, indicator_id=no_7.id, exceed_value=480, unit='mS/cm')
                 
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_1.id, exceed_value=9, unit='')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_2.id, exceed_value=270, unit='mv')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_3.id, exceed_value=29, unit='oC')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_6.id, exceed_value=33, unit='mg/l')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_7.id, exceed_value=10, unit='mg/l')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_8.id, exceed_value=480, unit='mS/cm')
    # db.qcvn_detail.insert(qcvn_id = st_3.id, qcvn_code ='QCVN 01-MT:2015/BTNMT',qcvn_type=0, indicator_id=no_9.id, exceed_value=480, unit='mS/cm')
           
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_1.id, exceed_value=50, unit='µg/m3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_2.id, exceed_value=350, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_3.id, exceed_value=1800, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_6.id, exceed_value=390, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_7.id, exceed_value=4, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_8.id, exceed_value=17, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_4.id,qcvn_code ='QCVN 12-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_9.id, exceed_value=4, unit='ppmC')
                 
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_1.id, exceed_value=50, unit='µg/m3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_2.id, exceed_value=350, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_3.id, exceed_value=1800, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_6.id, exceed_value=390, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_7.id, exceed_value=4, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_8.id, exceed_value=17, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_8.id, qcvn_code ='QCVN 28:2010/BTNMT', qcvn_type=0, indicator_id=no_9.id, exceed_value=4, unit='ppmC')
                 
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_1.id, exceed_value=50, unit='µg/m3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_2.id, exceed_value=350, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_3.id, exceed_value=1800, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_6.id, exceed_value=390, unit='mg/Nm3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_7.id, exceed_value=4, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_8.id, exceed_value=17, unit='ug/m3')
    # db.qcvn_detail.insert(qcvn_id = st_5.id, qcvn_code ='QCVN 13-MT:2015/BTNMT', qcvn_type=0, indicator_id=no_9.id, exceed_value=4, unit='ppmC')
    
  