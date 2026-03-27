#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 AI 智能体软件安装服务风险告知书 PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
import os

# 尝试注册中文字体
FONT_PATHS = [
    '/usr/share/fonts/google-noto-cjk/NotoSansCJKsc-Regular.otf',
    '/usr/share/fonts/google-noto-cjk/NotoSansCJKsc-Medium.otf',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

CHINESE_FONT = None
for font_path in FONT_PATHS:
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            CHINESE_FONT = 'ChineseFont'
            print(f"✅ 使用字体: {font_path}")
            break
        except:
            continue

if not CHINESE_FONT:
    print("⚠️ 未找到中文字体，使用默认字体")
    CHINESE_FONT = 'Helvetica'

def create_styles():
    """创建文档样式"""
    styles = getSampleStyleSheet()
    
    # 标题样式
    styles.add(ParagraphStyle(
        name='ChineseTitle',
        fontName=CHINESE_FONT,
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=10,
        leading=24
    ))
    
    # 副标题
    styles.add(ParagraphStyle(
        name='ChineseSubTitle',
        fontName=CHINESE_FONT,
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=15,
        spaceBefore=5,
        leading=20
    ))
    
    # 章节标题
    styles.add(ParagraphStyle(
        name='ChineseHeading',
        fontName=CHINESE_FONT,
        fontSize=12,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=15,
        leading=18,
        textColor=colors.darkblue
    ))
    
    # 正文样式
    styles.add(ParagraphStyle(
        name='ChineseBody',
        fontName=CHINESE_FONT,
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        spaceBefore=3,
        leading=16,
        firstLineIndent=20
    ))
    
    # 列表项样式
    styles.add(ParagraphStyle(
        name='ChineseItem',
        fontName=CHINESE_FONT,
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=4,
        spaceBefore=2,
        leading=15,
        leftIndent=20
    ))
    
    # 签名行样式
    styles.add(ParagraphStyle(
        name='ChineseSign',
        fontName=CHINESE_FONT,
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=5,
        spaceBefore=10,
        leading=14
    ))
    
    return styles

def build_document():
    """构建 PDF 文档"""
    output_path = '/root/.copaw/scripts/AI智能体软件安装服务_风险告知书.pdf'
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    styles = create_styles()
    story = []
    
    # ==================== 标题页 ====================
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("AI 智能体软件（OpenClaw 等）安装服务", styles['ChineseTitle']))
    story.append(Paragraph("风险告知书 + 免责协议 + 安全配置清单", styles['ChineseSubTitle']))
    story.append(Spacer(1, 1*cm))
    
    # ==================== 一、风险告知书 ====================
    story.append(Paragraph("一、风险告知书", styles['ChineseHeading']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("致：____________（客户名称）", styles['ChineseBody']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "本人/本单位自愿委托服务方安装 AI 智能体类软件（包括但不限于 OpenClaw、Moltbot、Qwen 等具备系统控制、自动执行能力的 AI 程序）。"
        "服务方已充分、清晰告知以下风险，本人/本单位已完全知晓、理解并自愿承担全部相关风险：",
        styles['ChineseBody']
    ))
    
    risks = [
        ("1. 系统高权限风险", 
         "AI 软件需获取系统文件读写、执行命令、调用 API、联网、安装程序等高权限，存在被恶意利用、远程控制、植入木马、挖矿、篡改系统的风险。"),
        ("2. 数据泄露与丢失风险", 
         "AI 可访问本地文件、账号密码、API 密钥、业务数据、个人信息等，若因配置不当、插件不安全、网络攻击等原因，可能导致数据泄露、丢失、被窃取。"),
        ("3. 第三方插件与模型风险", 
         "第三方插件、模型、脚本可能存在恶意代码、后门、漏洞，可能造成设备损坏、账号被盗、API 盗刷、隐私泄露。"),
        ("4. Prompt 注入与 AI 失控风险", 
         "AI 可能被恶意指令诱导，执行删除文件、修改配置、外传数据、违规操作等非预期行为，造成不可控后果。"),
        ("5. API 密钥泄露与费用失控风险", 
         "API Key 若保管不当，可能被盗用产生高额算力/调用费用，相关费用及责任由客户自行承担。"),
        ("6. 漏洞与网络攻击风险", 
         "此类软件属于高风险工具，存在公开漏洞，易遭受黑客攻击、入侵、exploit 利用，导致系统瘫痪或数据受损。"),
        ("7. 客户自身使用不当风险", 
         "客户自行修改配置、使用弱密码、对公网开放端口、随意安装不明插件、违规运行等行为引发的一切后果，均由客户自行承担。"),
    ]
    
    for title, content in risks:
        story.append(Paragraph(f"<b>{title}</b>", styles['ChineseItem']))
        story.append(Paragraph(content, styles['ChineseItem']))
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("<b>客户确认：</b>", styles['ChineseBody']))
    story.append(Paragraph(
        "本人已认真阅读并完全理解上述全部风险，自愿安装该类 AI 软件，并承担由此产生的一切后果。"
        "服务方仅提供软件安装、环境部署、基础配置等技术服务，不承担软件本身缺陷、攻击、使用不当造成的任何损失。",
        styles['ChineseBody']
    ))
    
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("客户签字/盖章：____________　　　　　　　日期：______年____月____日", styles['ChineseSign']))
    
    # ==================== 二、免责协议 ====================
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("二、免责协议", styles['ChineseHeading']))
    story.append(Spacer(1, 0.3*cm))
    
    agreement_items = [
        "1. 服务方仅提供<b>软件安装、环境调试、基础配置</b>技术服务，不提供任何安全性、稳定性、商用担保。",
        "2. 客户明确知晓 AI 智能体类软件属于<b>高权限、高风险工具</b>，并非标准化安全产品，存在固有安全风险。",
        "3. 因以下原因导致的任何直接或间接损失，服务方均不承担法律责任、赔偿责任：",
    ]
    
    for item in agreement_items:
        story.append(Paragraph(item, styles['ChineseBody']))
    
    sub_items = [
        "• 软件本身漏洞、缺陷、兼容性问题；",
        "• 第三方插件、模型、工具带来的恶意代码或安全问题；",
        "• 客户自行修改配置、使用弱密码、对公网开放端口、违规操作；",
        "• 黑客攻击、病毒入侵、Prompt 注入、网络劫持；",
        "• 数据丢失、密钥泄露、API 费用超支；",
        "• 客户业务系统、硬件、网络环境自身问题。",
    ]
    
    for sub in sub_items:
        story.append(Paragraph(sub, styles['ChineseItem']))
    
    story.append(Paragraph("4. 服务方已尽到充分风险告知义务，客户自愿接受并承担全部风险。", styles['ChineseBody']))
    story.append(Paragraph("5. 本协议自签字之日起生效，一式两份，双方各执一份。", styles['ChineseBody']))
    
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("客户签字/盖章：____________　　　　　　　服务方签字：____________", styles['ChineseSign']))
    story.append(Paragraph("日期：______年____月____日", styles['ChineseSign']))
    
    # ==================== 三、安全配置清单 ====================
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("三、安装安全配置 Checklist", styles['ChineseHeading']))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("服务方已完成以下基础安全配置（勾选确认）：", styles['ChineseBody']))
    story.append(Spacer(1, 0.3*cm))
    
    checklist_items = [
        "仅允许本地访问（127.0.0.1），禁止对公网开放端口",
        "启用强密码/密钥认证",
        "关闭自动安装第三方插件、自动执行高危命令",
        "避免以 root/管理员权限长期运行",
        "API Key 加密存储，不记录在日志、截图、明文配置",
        "关闭不必要的联网权限与自动更新",
        "限制 AI 访问敏感目录（桌面、文档、浏览器数据等）",
        "开启操作日志，便于追溯",
        "告知客户不随意安装来源不明插件",
        "告知客户定期更新、修改密码、备份数据",
    ]
    
    # 创建表格
    table_data = [["□", item] for item in checklist_items]
    
    table = Table(table_data, colWidths=[0.8*cm, 14*cm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    
    story.append(table)
    
    # 构建文档
    doc.build(story)
    print(f"\n✅ PDF 已生成: {output_path}")
    return output_path

if __name__ == '__main__':
    build_document()