def predict_reasons_try(comment):
    # Step 1: Embed the input comment using the SentenceTransformer
    vec = embedder.encode([comment], convert_to_numpy=True)

    # Step 2: Predict using the trained MultiOutputClassifier
    preds = model.predict(vec)[0]

    # Step 3: Build output
    flagged = any(preds)
    label_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    reasons = [label for label, p in zip(label_cols, preds) if p == 1]

    return {
        'flagged': int(flagged),
        'reasons': reasons
    }