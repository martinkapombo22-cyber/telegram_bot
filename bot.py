from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "8029553969:AAFvhA0GkZXGRw0mmEnWepCAJpZ_Ovey_q0"

NOM, PRENOM = range(2)


# -------- MENU PRINCIPAL --------
def main_menu():
    keyboard = [
        ["🚀 Découvrir nos Services"],
        ["🌐 Aller sur le Site", "📞 Contact Support"],
        ["❓ Aide & Infos"]
    ]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# -------- START --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur Mediabooster22 🚀\n\n"
        "Avant de commencer, quel est votre nom ?"
    )
    return NOM


# -------- DEMANDE PRENOM --------
async def ask_prenom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nom"] = update.message.text

    await update.message.reply_text(
        "Merci ! Quel est votre prénom ?"
    )

    return PRENOM


# -------- FIN INSCRIPTION --------
async def finish_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prenom = update.message.text
    nom = context.user_data["nom"]

    await update.message.reply_text(
        f"Bienvenue {prenom} {nom} 👋\n\n"
        "Que voulez-vous booster aujourd'hui ?",
        reply_markup=main_menu()
    )

    return ConversationHandler.END


# -------- GESTION MESSAGES --------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    text_lower = text.lower()

    if text == "🚀 Découvrir nos Services":
        await update.message.reply_text(
            "📈 Nos services disponibles :\n\n"
            "• Followers Instagram\n"
            "• Likes Instagram\n"
            "• Followers TikTok\n"
            "• Vues TikTok\n"
            "• Abonnés YouTube\n"
            "• Vues YouTube\n\n"
            "🌐 Commandez directement sur notre site :\n"
            "https://mediabooster22.com"
        )

    elif text == "📞 Contact Support":
        await update.message.reply_text(
            "📞 Support Mediabooster22\n\n"
            "Notre équipe est là pour vous accompagner.\n"
            "Telegram : @Mediabooster_Support\n"
            "Email : support@mediabooster22.com"
        )

    elif text == "🌐 Aller sur le Site":
        await update.message.reply_text(
            "🌐 Lien direct : https://mediabooster22.com"
        )

    elif text == "❓ Aide & Infos":
        await update.message.reply_text(
            "Besoin d'aide ?\n\n"
            "Utilisez les boutons du menu pour naviguer.\n"
            "Si vous avez une commande en cours, contactez le support."
        )

    elif any(w in text_lower for w in ["bonjour", "salut", "hello"]):
        await update.message.reply_text(
            "Bonjour 👋\nQue voulez-vous booster aujourd'hui ?",
            reply_markup=main_menu()
        )

    elif any(w in text_lower for w in ["acheter", "commander", "service"]):
        await update.message.reply_text(
            "🛒 Pour commander utilisez 'Découvrir nos Services' "
            "ou allez sur https://mediabooster22.com"
        )

    else:
        await update.message.reply_text(
            "Je ne suis pas sûr de comprendre 🤔\nUtilisez le menu ci-dessous.",
            reply_markup=main_menu()
        )


# -------- MAIN --------
def main():

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_prenom)],
            PRENOM: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_onboarding)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Mediabooster22 Bot est opérationnel")

    app.run_polling()


if name == "main":
    main()
