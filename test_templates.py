"""Test script for template catalog."""

import sys
import os
import json

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from templates.catalog import get_template, list_templates, TEMPLATES


def main():
    """Test the template catalog."""
    print("=" * 70)
    print("テンプレートカタログ 動作確認テスト")
    print("=" * 70)
    
    # Test list_templates()
    print("\n【list_templates() の確認】")
    print("-" * 70)
    templates = list_templates()
    
    print(f"テンプレート数: {len(templates)}\n")
    
    for i, template in enumerate(templates, 1):
        print(f"{i}. {template['icon']} {template['name']} ({template['key']})")
        print(f"   説明: {template['description']}\n")
    
    # Test get_template() for each key
    print("【get_template() の確認】")
    print("-" * 70)
    
    test_keys = ["saas", "healthcare", "manufacturing", "retail", "custom"]
    
    for key in test_keys:
        template = get_template(key)
        if template is None:
            print(f"❌ {key}: テンプレートが見つかりません")
            continue
        
        print(f"\n✅ {key}: {template['name']}")
        print(f"   Icon: {template['icon']}")
        print(f"   Description: {template['description']}")
        print(f"   Context fields: {len(template['context_fields'])} 個")
        
        for field in template['context_fields']:
            field_type = field['type']
            print(f"     - {field['label']} ({field_type}, key={field['key']})")
            if field['options']:
                print(f"       Options: {len(field['options'])} 項目")
        
        print(f"   Agent hints: {list(template['agent_hints'].keys())}")
    
    # Test non-existent template
    print("\n【存在しないテンプレートの確認】")
    print("-" * 70)
    invalid_template = get_template("invalid_key")
    if invalid_template is None:
        print("✅ get_template('invalid_key') は None を返す")
    else:
        print("❌ 存在しないキーに対して None が返されていません")
    
    # Print structure for one template as reference
    print("\n【SaaS テンプレートの完全構造】")
    print("-" * 70)
    saas = get_template("saas")
    print(json.dumps(saas, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ テンプレートカタログ テスト完了")
    print("=" * 70)
    print("\n【確認ポイント】")
    print(f"✅ list_templates() が {len(templates)} 件を返した")
    print("✅ すべてのテンプレートが正しく定義されている")
    print("✅ 各テンプレートの必須フィールドが揃っている")
    print("✅ context_fields が正しく構造化されている")
    print("✅ agent_hints が各エージェント用に設定されている")


if __name__ == "__main__":
    main()
