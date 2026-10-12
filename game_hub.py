import streamlit as st
import random

# 设置网页的基本信息
st.set_page_config(page_title="攸宁和怀瑾的游戏盒子", page_icon="🎮", layout="centered")

# 在左侧边栏做一个游戏选择器（像个菜单一样喵）
st.sidebar.title("🎐 攸宁和怀瑾的游戏盒子")
st.sidebar.write("今天想玩点什么喵？")
game_choice = st.sidebar.radio("请选择游戏：", ["🔢 猜数字", "🀄 文字消消乐"])

st.write("---")

# ================= 游戏 1：猜数字 =================
if game_choice == "🔢 猜数字":
    st.header("🔢 攸宁的猜数字游戏")
    st.write("攸宁想好了一个 1 到 100 之间的数字，猜猜看嘛~")

    # 初始化小记忆
    if 'target' not in st.session_state:
        st.session_state.target = random.randint(1, 100)
        st.session_state.count = 0
        st.session_state.win = False
        st.session_state.msg = ""

    guess = st.number_input("请输入你猜的数字：", min_value=1, max_value=100, step=1)

    if st.button("提交猜测"):
        if not st.session_state.win:
            st.session_state.count += 1
            if guess == st.session_state.target:
                st.session_state.msg = f"🎉 猜对了喵！答案是 {st.session_state.target}，你花了 {st.session_state.count} 次！"
                st.session_state.win = True
            elif st.session_state.count >= 5:
                st.session_state.msg = f"😿 呜呜，5次机会用完啦，答案是 {st.session_state.target}。"
                st.session_state.win = True
            elif guess > st.session_state.target:
                st.session_state.msg = f"📈 太大啦！还剩 {5 - st.session_state.count} 次机会喵。"
            elif guess < st.session_state.target:
                st.session_state.msg = f"📉 太小啦！还剩 {5 - st.session_state.count} 次机会喵。"

    if st.session_state.msg:
        st.info(st.session_state.msg)

    if st.session_state.win:
        if st.button("再陪我玩一局嘛！"):
            st.session_state.target = random.randint(1, 100)
            st.session_state.count = 0
            st.session_state.win = False
            st.session_state.msg = ""
            st.rerun()

# ================= 游戏 2：文字消消乐 =================
elif game_choice == "🀄 文字消消乐":
    st.header("🀄 文字消消乐")
    
    # 增加难度选择
    difficulty = st.radio("选择难度喵：", ["🌱 普通模式", "🔥 地狱模式"], horizontal=True)
    
    # 设定不同难度的参数
    if difficulty == "🌱 普通模式":
        pairs_count = 4
        max_attempts = 5
        st.write(f"点开两张卡片，找到一样的文字消除。你只有 {max_attempts} 次机会喵！")
    else:
        pairs_count = 8
        max_attempts = 999 # 无限次
        st.write("地狱模式启动！只要翻错，全场洗牌重排！你准备好了吗？")

    # 初始化游戏状态
    if 'game_mode' not in st.session_state or st.session_state.game_mode != difficulty:
        base_cards = ["🐱", "🐶", "🐰", "🐼", "🦊", "🐸", "🐨", "🐯"][:pairs_count]
        cards = base_cards * 2
        random.shuffle(cards)
        
        st.session_state.cards = cards
        st.session_state.revealed = []
        st.session_state.matched = []
        st.session_state.attempts = 0
        st.session_state.game_mode = difficulty
        st.session_state.defeated = False

    # 游戏失败画面
    if st.session_state.defeated:
        st.error("😿 失败啦！")
        st.write("杂口,杂口,这还用五次也太杂鱼了吧.")
        if st.button("我不服，再来一局！"):
            del st.session_state.game_mode # 强制重置
            st.rerun()
        st.stop()

    # 生成卡片网格
    cols = st.columns(4)
    
    for i, card in enumerate(st.session_state.cards):
        if i in st.session_state.matched:
            cols[i % 4].button("✅", key=f"btn_{i}", disabled=True)
        elif i in st.session_state.revealed:
            if cols[i % 4].button(card, key=f"btn_{i}"):
                pass
        else:
            if cols[i % 4].button("❓", key=f"btn_{i}"):
                st.session_state.revealed.append(i)
                
                # 翻开两张牌，开始判断
                if len(st.session_state.revealed) == 2:
                    idx1 = st.session_state.revealed[0]
                    idx2 = st.session_state.revealed[1]
                    
                    if st.session_state.cards[idx1] == st.session_state.cards[idx2]:
                        # 配对成功
                        st.session_state.matched.extend([idx1, idx2])
                        st.session_state.revealed = []
                        st.balloons()
                    else:
                        # 配对失败
                        st.session_state.attempts += 1
                        if difficulty == "🌱 普通模式":
                            if st.session_state.attempts >= max_attempts:
                                st.session_state.defeated = True
                            else:
                                st.session_state.revealed = [] # 只是盖回去
                        else:
                            # 地狱模式：翻错直接洗牌！
                            st.session_state.revealed = []
                            # 把没消除的牌拿出来重新洗牌
                            remaining_cards = [st.session_state.cards[i] for i in range(len(st.session_state.cards)) if i not in st.session_state.matched]
                            random.shuffle(remaining_cards)
                            # 覆盖回去（保留已消除的牌的位置）
                            idx_counter = 0
                            for j in range(len(st.session_state.cards)):
                                if j not in st.session_state.matched:
                                    st.session_state.cards[j] = remaining_cards[idx_counter]
                                    idx_counter += 1
                            st.toast("😈 翻错啦！地狱模式洗牌重来！")
                st.rerun()

    # 胜利判定
    if len(st.session_state.matched) == len(st.session_state.cards):
        st.success("🎉 哇！宝宝全部消除成功啦！你太厉害了喵！")
        if st.button("再玩一次"):
            del st.session_state.game_mode
            st.rerun()