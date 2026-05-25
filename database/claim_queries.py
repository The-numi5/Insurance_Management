from database.connection import get_connection


def add_claim(user_policy_id, amount, status="Pending"):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO CLAIMS (user_policy_id, amount, status)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (user_policy_id, amount, status))
    conn.commit()
    conn.close()


def get_user_claims(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        c.claim_id,
        p.policy_name,
        c.amount,
        c.status
    FROM CLAIMS c
    JOIN USER_POLICIES up ON c.user_policy_id = up.purchase_id
    JOIN POLICIES p ON up.policy_id = p.policy_id
    WHERE up.user_id = %s
    """
    cursor.execute(query, (user_id,))
    claims = cursor.fetchall()
    conn.close()
    return claims


def get_all_claims():
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT 
        c.claim_id,
        u.username,
        p.policy_name,
        c.amount,
        c.status
    FROM CLAIMS c
    JOIN USER_POLICIES up ON c.user_policy_id = up.purchase_id
    JOIN USERS u ON up.user_id = u.user_id
    JOIN POLICIES p ON up.policy_id = p.policy_id
    """
    cursor.execute(query)
    claims = cursor.fetchall()
    conn.close()
    return claims


def update_claim_status(claim_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    UPDATE CLAIMS
    SET status = %s
    WHERE claim_id = %s
    """
    cursor.execute(query, (new_status, claim_id))
    conn.commit()
    conn.close()

def get_agent_claims(agent_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT claim_id, policy_id, claim_amount, status
    FROM CLAIMS
    WHERE agent_id = %s
    """

    cursor.execute(query, (agent_id,))
    claims = cursor.fetchall()

    cursor.close()
    conn.close()
    return claims